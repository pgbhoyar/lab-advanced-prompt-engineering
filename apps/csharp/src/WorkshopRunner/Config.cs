namespace WorkshopRunner;

public sealed class ConfigException : Exception
{
    public ConfigException(string message) : base(message) { }
}

/// <summary>Configuration loaded from environment variables. Never exposes the API key.</summary>
public sealed record Config(
    string BaseUrl,
    string ApiKey,
    string Deployment,
    string ReasoningEffort,
    int MaxOutputTokens,
    int RequestTimeoutSeconds,
    bool SaveResults,
    string ResultsDirectory)
{
    private static readonly string[] Required =
        { "AZURE_OPENAI_BASE_URL", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_DEPLOYMENT" };

    public static Config Load(IDictionary<string, string?>? env = null)
    {
        string? Get(string k) => env is null ? Environment.GetEnvironmentVariable(k) : (env.TryGetValue(k, out var v) ? v : null);

        var missing = Required.Where(k => string.IsNullOrWhiteSpace(Get(k))).ToList();
        if (missing.Count > 0)
            throw new ConfigException(
                "Missing required environment variable(s): " + string.Join(", ", missing) +
                ". Copy .env.example to .env and fill in the workshop values.");

        var baseUrl = Get("AZURE_OPENAI_BASE_URL")!.Trim();
        var apiKey = Get("AZURE_OPENAI_API_KEY")!.Trim();
        var deployment = Get("AZURE_OPENAI_DEPLOYMENT")!.Trim();

        if (apiKey.Contains('<') && apiKey.Contains('>'))
            throw new ConfigException("AZURE_OPENAI_API_KEY still contains a placeholder. Paste the real workshop key.");
        if (!baseUrl.StartsWith("https://", StringComparison.OrdinalIgnoreCase))
            throw new ConfigException("AZURE_OPENAI_BASE_URL must use https://.");
        if (!baseUrl.TrimEnd('/').EndsWith("/openai/v1", StringComparison.OrdinalIgnoreCase))
            throw new ConfigException("AZURE_OPENAI_BASE_URL must end in /openai/v1/ (the v1 Responses API base).");
        if (string.IsNullOrWhiteSpace(deployment))
            throw new ConfigException("AZURE_OPENAI_DEPLOYMENT must not be blank.");

        int ParseInt(string k, int dflt)
        {
            var raw = Get(k);
            if (string.IsNullOrWhiteSpace(raw)) return dflt;
            if (!int.TryParse(raw, out var val) || val <= 0)
                throw new ConfigException($"{k} must be a positive integer.");
            return val;
        }

        return new Config(
            baseUrl, apiKey, deployment,
            (Get("WORKSHOP_REASONING_EFFORT") ?? "low").Trim(),
            ParseInt("WORKSHOP_MAX_OUTPUT_TOKENS", 800),
            ParseInt("WORKSHOP_REQUEST_TIMEOUT_SECONDS", 90),
            string.Equals((Get("WORKSHOP_SAVE_RESULTS") ?? "false").Trim(), "true", StringComparison.OrdinalIgnoreCase),
            (Get("WORKSHOP_RESULTS_DIRECTORY") ?? "generated-results").Trim());
    }

    public string Redacted() =>
        $"base_url={BaseUrl}, api_key=***redacted***, deployment={Deployment}, " +
        $"reasoning_effort={ReasoningEffort}, max_output_tokens={MaxOutputTokens}";
}
