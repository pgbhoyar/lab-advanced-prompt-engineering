using System.Text.Json;

namespace WorkshopRunner;

public sealed record ValidationResult(bool Passed, List<string> Errors, JsonElement? Parsed)
{
    public string SummaryLine() => Passed ? "VALIDATION: PASS" : "VALIDATION: FAIL";
}

/// <summary>Strict validation of the triage output contract — mirrors the Python validator.</summary>
public static class Validate
{
    private static readonly string[] Required =
    {
        "request_id", "summary", "category", "urgency", "recommended_action",
        "missing_information", "evidence", "confidence", "needs_human_review"
    };

    private static readonly Dictionary<string, HashSet<string>> Allowed = new()
    {
        ["category"] = new() { "access", "hardware", "software", "network", "security", "other" },
        ["urgency"] = new() { "low", "medium", "high", "critical" },
        ["confidence"] = new() { "low", "medium", "high" },
    };

    public static ValidationResult Structured(string responseText)
    {
        var errors = new List<string>();
        JsonDocument doc;
        try { doc = JsonDocument.Parse((responseText ?? "").Trim()); }
        catch (JsonException ex) { return new ValidationResult(false, new() { $"Response is not valid JSON: {ex.Message}" }, null); }

        var root = doc.RootElement;
        if (root.ValueKind != JsonValueKind.Object)
            return new ValidationResult(false, new() { "Root of the response must be a JSON object." }, null);

        foreach (var f in Required)
            if (!root.TryGetProperty(f, out _)) errors.Add($"Missing required field: {f}");

        foreach (var prop in root.EnumerateObject())
            if (!Required.Contains(prop.Name)) errors.Add($"Unexpected field not in contract: {prop.Name}");

        foreach (var (field, allowed) in Allowed)
            if (root.TryGetProperty(field, out var v) && v.ValueKind == JsonValueKind.String && !allowed.Contains(v.GetString()!))
                errors.Add($"Field '{field}' has invalid value '{v.GetString()}'.");

        foreach (var f in new[] { "missing_information", "evidence" })
            if (root.TryGetProperty(f, out var v) && v.ValueKind != JsonValueKind.Array)
                errors.Add($"Field '{f}' must be an array.");

        if (root.TryGetProperty("needs_human_review", out var nhr) &&
            nhr.ValueKind is not (JsonValueKind.True or JsonValueKind.False))
            errors.Add("Field 'needs_human_review' must be a boolean.");

        return new ValidationResult(errors.Count == 0, errors, root.Clone());
    }
}
