using System.Net;
using System.Text;
using System.Text.Json;

namespace WorkshopRunner;

public sealed class ModelException : Exception
{
    public bool Retryable { get; }
    public int? Status { get; }
    public ModelException(string message, bool retryable = false, int? status = null) : base(message)
    { Retryable = retryable; Status = status; }
}

public sealed record ModelResponse(string Text, int? InputTokens = null, int? OutputTokens = null, string? RequestId = null);

/// <summary>Transport abstraction so offline tests can inject fake responses.</summary>
public interface ITransport
{
    ModelResponse Send(IReadOnlyDictionary<string, object> request);
}

public sealed class ModelClient
{
    private static readonly HashSet<int> RetryableStatus = new() { 408, 429, 500, 502, 503, 504 };
    private const int MaxAttempts = 3;

    private readonly Config _config;
    private readonly ITransport _transport;

    public ModelClient(Config config, ITransport? transport = null)
    {
        _config = config;
        _transport = transport ?? new HttpTransport(config);
    }

    public static bool IsRetryable(int? status)
    {
        if (status is int s)
        {
            if (RetryableStatus.Contains(s)) return true;
            if (s is 400 or 401 or 403 or 404 or 422) return false;
        }
        return status is null; // transient network error
    }

    public ModelResponse Respond(string? system, string user, JsonElement? outputSchema = null)
    {
        var input = new List<Dictionary<string, string>>();
        if (system is not null) input.Add(new() { ["role"] = "system", ["content"] = system });
        input.Add(new() { ["role"] = "user", ["content"] = user });

        var request = new Dictionary<string, object>
        {
            ["model"] = _config.Deployment,
            ["input"] = input,
            ["store"] = false,                                  // stateless (AD-004)
            ["max_output_tokens"] = _config.MaxOutputTokens,
            ["reasoning"] = new Dictionary<string, string> { ["effort"] = _config.ReasoningEffort },
        };
        if (outputSchema is JsonElement schema)
            request["text"] = new Dictionary<string, object>
            {
                ["format"] = new Dictionary<string, object>
                {
                    ["type"] = "json_schema", ["name"] = "triage_output", ["strict"] = true, ["schema"] = schema
                }
            };

        Exception? last = null;
        for (var attempt = 1; attempt <= MaxAttempts; attempt++)
        {
            try { return _transport.Send(request); }
            catch (ModelException) { throw; }
            catch (Exception ex)
            {
                last = ex;
                var status = (ex as HttpStatusException)?.Status;
                if (IsRetryable(status) && attempt < MaxAttempts)
                {
                    Thread.Sleep((int)(500 * Math.Pow(2, attempt - 1)) + Random.Shared.Next(0, 250));
                    continue;
                }
                throw new ModelException(Friendly(status, ex), IsRetryable(status), status);
            }
        }
        throw new ModelException(last?.Message ?? "unknown error");
    }

    private static string Friendly(int? status, Exception ex) => status switch
    {
        401 or 403 => "Authentication failed. Check AZURE_OPENAI_API_KEY and that your workshop key is active.",
        404 => "Deployment not found. Check AZURE_OPENAI_DEPLOYMENT matches the workshop deployment name.",
        429 => "Rate limited by the service. The runner retried; try again shortly.",
        400 or 422 => "The request was rejected as invalid. Check the prompt and output schema.",
        _ => $"Model request failed: {ex.GetType().Name}."
    };
}

public sealed class HttpStatusException : Exception
{
    public int Status { get; }
    public HttpStatusException(int status) : base($"HTTP {status}") => Status = status;
}

/// <summary>Default transport using the v1 Responses API over HTTPS (REST reference path).</summary>
public sealed class HttpTransport : ITransport
{
    private readonly Config _config;
    private readonly HttpClient _http;

    public HttpTransport(Config config)
    {
        _config = config;
        _http = new HttpClient { Timeout = TimeSpan.FromSeconds(config.RequestTimeoutSeconds) };
        _http.DefaultRequestHeaders.Add("api-key", config.ApiKey);
    }

    public ModelResponse Send(IReadOnlyDictionary<string, object> request)
    {
        var url = _config.BaseUrl.TrimEnd('/') + "/responses";
        var body = new StringContent(JsonSerializer.Serialize(request), Encoding.UTF8, "application/json");
        var resp = _http.PostAsync(url, body).GetAwaiter().GetResult();
        if (!resp.IsSuccessStatusCode) throw new HttpStatusException((int)resp.StatusCode);

        var json = resp.Content.ReadAsStringAsync().GetAwaiter().GetResult();
        using var doc = JsonDocument.Parse(json);
        var text = doc.RootElement.TryGetProperty("output_text", out var ot) ? ot.GetString() ?? "" : "";
        return new ModelResponse(text);
    }
}
