using System.Text.Json;

namespace WorkshopRunner;

public sealed class CaseException : Exception
{
    public CaseException(string message) : base(message) { }
}

public sealed record TestCase(string Id, string ScenarioType, Dictionary<string, string> Input);

public static class Cases
{
    public static List<TestCase> Load(string path)
    {
        if (!File.Exists(path)) throw new CaseException($"Test set not found: {path}");
        var list = new List<TestCase>();
        var lineNo = 0;
        foreach (var raw in File.ReadLines(path))
        {
            lineNo++;
            var line = raw.Trim();
            if (line.Length == 0) continue;
            try
            {
                using var doc = JsonDocument.Parse(line);
                var root = doc.RootElement;
                var input = new Dictionary<string, string>();
                foreach (var p in root.GetProperty("input").EnumerateObject())
                    input[p.Name] = p.Value.ValueKind == JsonValueKind.String ? p.Value.GetString()! : p.Value.ToString();
                list.Add(new TestCase(root.GetProperty("id").GetString()!,
                                      root.GetProperty("scenario_type").GetString()!, input));
            }
            catch (JsonException ex)
            {
                throw new CaseException($"Invalid JSON on line {lineNo} of {path}: {ex.Message}");
            }
        }
        return list;
    }

    public static TestCase Find(string path, string caseId)
    {
        var c = Load(path).FirstOrDefault(x => x.Id == caseId);
        return c ?? throw new CaseException($"Test case '{caseId}' not found in {path}");
    }
}
