using System.Text.Json;
using WorkshopRunner;
using Xunit;

namespace WorkshopRunner.Tests;

[Trait("Category", "Offline")]
public class OfflineTests
{
    private static Dictionary<string, string?> GoodEnv() => new()
    {
        ["AZURE_OPENAI_BASE_URL"] = "https://example.openai.azure.com/openai/v1/",
        ["AZURE_OPENAI_API_KEY"] = "abcd1234abcd1234abcd1234abcd1234",
        ["AZURE_OPENAI_DEPLOYMENT"] = "workshop-gpt-54",
    };

    private const string ValidTriage =
        "{\"request_id\":\"SR-1\",\"summary\":\"x\",\"category\":\"network\",\"urgency\":\"high\"," +
        "\"recommended_action\":\"do x\",\"missing_information\":[],\"evidence\":[]," +
        "\"confidence\":\"medium\",\"needs_human_review\":false}";

    [Fact]
    public void ConfigLoadsAndRedacts()
    {
        var cfg = Config.Load(GoodEnv());
        Assert.Equal("workshop-gpt-54", cfg.Deployment);
        Assert.Contains("***redacted***", cfg.Redacted());
    }

    [Theory]
    [InlineData("AZURE_OPENAI_API_KEY", "", "Missing required")]
    [InlineData("AZURE_OPENAI_BASE_URL", "http://x/openai/v1/", "https")]
    [InlineData("AZURE_OPENAI_BASE_URL", "https://x/openai/", "/openai/v1/")]
    [InlineData("AZURE_OPENAI_API_KEY", "<placeholder>", "placeholder")]
    public void ConfigRejectsBadValues(string key, string value, string expected)
    {
        var env = GoodEnv();
        env[key] = value;
        var ex = Assert.Throws<ConfigException>(() => Config.Load(env));
        Assert.Contains(expected, ex.Message, StringComparison.OrdinalIgnoreCase);
    }

    [Fact]
    public void ConfigErrorNeverContainsKey()
    {
        var env = GoodEnv();
        env["AZURE_OPENAI_BASE_URL"] = "http://x/openai/v1/";
        var ex = Assert.Throws<ConfigException>(() => Config.Load(env));
        Assert.DoesNotContain("abcd1234", ex.Message);
    }

    [Fact]
    public void ValidateSuccessStructured()
    {
        var r = Validate.Structured(ValidTriage);
        Assert.True(r.Passed);
        Assert.Empty(r.Errors);
    }

    [Fact]
    public void ValidateInvalidJson()
    {
        var r = Validate.Structured("category is network, urgency high");
        Assert.False(r.Passed);
        Assert.Contains(r.Errors, e => e.Contains("not valid JSON"));
    }

    [Fact]
    public void ValidateSchemaViolation()
    {
        var bad = "{\"request_id\":\"SR-1\",\"summary\":\"x\",\"category\":\"network\",\"urgency\":\"urgent\"," +
                  "\"recommended_action\":\"a\",\"missing_information\":[],\"evidence\":[],\"confidence\":\"low\"," +
                  "\"needs_human_review\":false,\"extra\":1}";
        var r = Validate.Structured(bad);
        Assert.False(r.Passed);
        Assert.Contains(r.Errors, e => e.Contains("urgency"));
        Assert.Contains(r.Errors, e => e.Contains("extra"));
    }

    private sealed class FlakyTransport : ITransport
    {
        private int _calls;
        private readonly int _failTimes;
        public int Calls => _calls;
        public FlakyTransport(int failTimes) => _failTimes = failTimes;
        public ModelResponse Send(IReadOnlyDictionary<string, object> request)
        {
            _calls++;
            if (_calls <= _failTimes) throw new HttpStatusException(429);
            return new ModelResponse(ValidTriage);
        }
    }

    [Fact]
    public void RetryThenSuccess()
    {
        var transport = new FlakyTransport(2);
        var client = new ModelClient(Config.Load(GoodEnv()), transport);
        var resp = client.Respond(null, "hi");
        Assert.Equal(3, transport.Calls);
        using var doc = JsonDocument.Parse(resp.Text);
        Assert.Equal("network", doc.RootElement.GetProperty("category").GetString());
    }

    private sealed class AuthFailTransport : ITransport
    {
        public ModelResponse Send(IReadOnlyDictionary<string, object> request) => throw new HttpStatusException(401);
    }

    [Fact]
    public void AuthFailureNotRetried()
    {
        var client = new ModelClient(Config.Load(GoodEnv()), new AuthFailTransport());
        var ex = Assert.Throws<ModelException>(() => client.Respond(null, "hi"));
        Assert.Equal(401, ex.Status);
        Assert.False(ex.Retryable);
    }

    private sealed class CaptureTransport : ITransport
    {
        public IReadOnlyDictionary<string, object>? Captured;
        public ModelResponse Send(IReadOnlyDictionary<string, object> request)
        { Captured = request; return new ModelResponse(ValidTriage); }
    }

    [Fact]
    public void RequestOmitsUnsupportedParamsAndIsStateless()
    {
        var t = new CaptureTransport();
        new ModelClient(Config.Load(GoodEnv()), t).Respond("sys", "usr");
        Assert.False((bool)t.Captured!["store"]);
        foreach (var banned in new[] { "temperature", "top_p", "presence_penalty", "frequency_penalty" })
            Assert.False(t.Captured!.ContainsKey(banned));
    }

    [Theory]
    [InlineData(503, true)]
    [InlineData(400, false)]
    [InlineData(null, true)]
    public void RetryClassification(int? status, bool expected)
        => Assert.Equal(expected, ModelClient.IsRetryable(status));
}
