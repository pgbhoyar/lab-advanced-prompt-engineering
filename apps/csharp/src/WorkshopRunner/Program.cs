using System.Text.Json;

namespace WorkshopRunner;

public static class Program
{
    private const int ExitOk = 0, ExitUsage = 1, ExitConfig = 2, ExitModel = 3, ExitValidation = 4;

    public static int Main(string[] args)
    {
        if (args.Length == 0) { Console.Error.WriteLine("Usage: <command> [options]"); return ExitUsage; }
        var cmd = args[0];
        var opts = ParseOptions(args);
        try
        {
            return cmd switch
            {
                "check-config" => CheckConfig(),
                "list-labs" => ListLabs(),
                "list-cases" => ListCases(opts),
                "run" => Run(opts),
                "validate" => Validate(opts),
                _ => Usage($"Unknown command: {cmd}")
            };
        }
        catch (ConfigException ex) { Console.Error.WriteLine($"Config error: {ex.Message}"); return ExitConfig; }
    }

    private static int Usage(string msg) { Console.Error.WriteLine(msg); return ExitUsage; }

    private static Dictionary<string, string> ParseOptions(string[] args)
    {
        var d = new Dictionary<string, string>();
        for (var i = 1; i < args.Length; i++)
        {
            if (args[i].StartsWith("--"))
            {
                var key = args[i][2..];
                if (i + 1 < args.Length && !args[i + 1].StartsWith("--")) { d[key] = args[++i]; }
                else d[key] = "true";
            }
        }
        return d;
    }

    private static int CheckConfig()
    {
        var cfg = Config.Load();
        Console.WriteLine("Config OK: " + cfg.Redacted());
        return ExitOk;
    }

    private static int ListLabs()
    {
        var root = RepoRoot.Find();
        foreach (var lab in Prompts.IterManifests(root).Select(m => m.Lab).Distinct().OrderBy(x => x))
            Console.WriteLine(lab);
        return ExitOk;
    }

    private static int ListCases(Dictionary<string, string> o)
    {
        if (!o.TryGetValue("lab", out var lab)) return Usage("--lab is required");
        var root = RepoRoot.Find();
        var manifests = Prompts.IterManifests(root).Where(m => m.Lab == lab).ToList();
        var testSet = manifests.FirstOrDefault(m => m.TestSet is not null)?.TestSet;
        if (testSet is null) return Usage($"No test_set for lab '{lab}'.");
        var dir = manifests.First(m => m.TestSet is not null).Dir;
        foreach (var c in Cases.Load(Path.GetFullPath(Path.Combine(dir, testSet))))
            Console.WriteLine($"{c.Id}\t{c.ScenarioType}");
        return ExitOk;
    }

    private static int Run(Dictionary<string, string> o)
    {
        if (!o.TryGetValue("lab", out var lab) || !o.TryGetValue("case", out var caseId) || !o.TryGetValue("variant", out var variant))
            return Usage("--lab, --case, and --variant are required");

        var cfg = Config.Load();
        var root = RepoRoot.Find();
        var manifest = Prompts.IterManifests(root).FirstOrDefault(m => m.Lab == lab && m.Variant == variant);
        if (manifest is null) return Usage($"No manifest for lab '{lab}' variant '{variant}'.");
        if (manifest.TestSet is null) return Usage($"Manifest {manifest.Id} has no test_set.");

        var testCase = Cases.Find(Path.GetFullPath(Path.Combine(manifest.Dir, manifest.TestSet)), caseId);
        var prompt = Prompts.Build(manifest, testCase.Input);

        Console.WriteLine($"Lab={manifest.Lab} case={testCase.Id} variant={manifest.Variant} prompt={manifest.Id}@{manifest.Version}");
        if (!o.ContainsKey("quiet"))
        {
            if (prompt.System is not null) Console.WriteLine("\n--- SYSTEM ---\n" + prompt.System);
            Console.WriteLine("\n--- USER ---\n" + prompt.User);
        }

        JsonElement? schema = null;
        if (manifest.OutputSchema is not null)
        {
            using var sd = JsonDocument.Parse(File.ReadAllText(Path.GetFullPath(Path.Combine(manifest.Dir, manifest.OutputSchema))));
            schema = sd.RootElement.Clone();
        }

        var client = new ModelClient(cfg);
        ModelResponse resp;
        try { resp = client.Respond(prompt.System, prompt.User, schema); }
        catch (ModelException ex) { Console.Error.WriteLine($"Model error: {ex.Message}"); return ExitModel; }

        Console.WriteLine("\n--- RESPONSE ---\n" + resp.Text);

        if (schema is not null)
        {
            var v = WorkshopRunner.Validate.Structured(resp.Text);
            Console.WriteLine("\n" + v.SummaryLine());
            foreach (var e in v.Errors) Console.Error.WriteLine($"  - {e}");
            if (!v.Passed) return ExitValidation;
        }
        return ExitOk;
    }

    private static int Validate(Dictionary<string, string> o)
    {
        string text = o.TryGetValue("file", out var file) ? File.ReadAllText(file) : Console.In.ReadToEnd();
        try
        {
            using var doc = JsonDocument.Parse(text);
            if (doc.RootElement.ValueKind == JsonValueKind.Object && doc.RootElement.TryGetProperty("parsed_output", out var po))
                text = po.GetRawText();
        }
        catch (JsonException) { /* validate as-is */ }

        var v = WorkshopRunner.Validate.Structured(text);
        Console.WriteLine(v.SummaryLine());
        foreach (var e in v.Errors) Console.Error.WriteLine($"  - {e}");
        return v.Passed ? ExitOk : ExitValidation;
    }
}
