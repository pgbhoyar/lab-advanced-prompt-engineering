using System.Text.RegularExpressions;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace WorkshopRunner;

public sealed class PromptException : Exception
{
    public PromptException(string message) : base(message) { }
}

public sealed class PromptManifest
{
    public string Id { get; set; } = "";
    public string Version { get; set; } = "";
    public string Lab { get; set; } = "";
    public string Variant { get; set; } = "";
    public string Purpose { get; set; } = "";
    [YamlMember(Alias = "system_prompt")] public string? SystemPrompt { get; set; }
    [YamlMember(Alias = "user_prompt")] public string UserPrompt { get; set; } = "";
    public List<string> Variables { get; set; } = new();
    [YamlMember(Alias = "output_schema")] public string? OutputSchema { get; set; }
    [YamlMember(Alias = "test_set")] public string? TestSet { get; set; }

    [YamlIgnore] public string Dir { get; set; } = ".";
}

public sealed record RenderedPrompt(string? System, string User);

public static class Prompts
{
    private static readonly Regex Placeholder = new(@"\{\{\s*([a-z0-9_]+)\s*\}\}", RegexOptions.Compiled);
    private static readonly IDeserializer Yaml =
        new DeserializerBuilder().WithNamingConvention(UnderscoredNamingConvention.Instance)
            .IgnoreUnmatchedProperties().Build();

    public static IEnumerable<PromptManifest> IterManifests(string repoRoot)
    {
        var dir = Path.Combine(repoRoot, "prompts");
        if (!Directory.Exists(dir)) yield break;
        foreach (var mf in Directory.EnumerateFiles(dir, "*.manifest.yaml", SearchOption.AllDirectories).OrderBy(x => x))
        {
            PromptManifest? m = null;
            try { m = LoadManifest(mf); } catch { /* skip malformed */ }
            if (m is not null) yield return m;
        }
    }

    public static PromptManifest LoadManifest(string path)
    {
        if (!File.Exists(path)) throw new PromptException($"Manifest not found: {path}");
        var m = Yaml.Deserialize<PromptManifest>(File.ReadAllText(path))
                ?? throw new PromptException($"Empty manifest: {path}");
        m.Dir = Path.GetDirectoryName(Path.GetFullPath(path))!;
        return m;
    }

    public static string Render(string template, IReadOnlyDictionary<string, string> values, IReadOnlyList<string> declared)
    {
        var used = Placeholder.Matches(template).Select(x => x.Groups[1].Value).ToHashSet();
        var undeclared = used.Except(declared).ToList();
        if (undeclared.Count > 0)
            throw new PromptException("Prompt uses undeclared variable(s): " + string.Join(", ", undeclared));

        return Placeholder.Replace(template, m =>
        {
            var name = m.Groups[1].Value;
            if (!values.TryGetValue(name, out var v))
                throw new PromptException($"Missing value for variable: {name}");
            return v;
        });
    }

    public static RenderedPrompt Build(PromptManifest manifest, IReadOnlyDictionary<string, string> values)
    {
        string Read(string rel)
        {
            var fp = Path.GetFullPath(Path.Combine(manifest.Dir, rel));
            if (!File.Exists(fp)) throw new PromptException($"Referenced prompt file not found: {fp}");
            return File.ReadAllText(fp);
        }

        string? system = manifest.SystemPrompt is null ? null : Render(Read(manifest.SystemPrompt), values, manifest.Variables);
        string user = Render(Read(manifest.UserPrompt), values, manifest.Variables);
        return new RenderedPrompt(system, user);
    }
}
