namespace WorkshopRunner;

/// <summary>Locates the repository root that holds the shared prompts/, schemas/, datasets/.</summary>
public static class RepoRoot
{
    public static string Find()
    {
        var env = Environment.GetEnvironmentVariable("WORKSHOP_REPO_ROOT");
        if (!string.IsNullOrWhiteSpace(env)) return env;

        var dir = new DirectoryInfo(AppContext.BaseDirectory);
        while (dir is not null)
        {
            if (Directory.Exists(Path.Combine(dir.FullName, "prompts")) &&
                Directory.Exists(Path.Combine(dir.FullName, "schemas")))
                return dir.FullName;
            dir = dir.Parent;
        }
        // Fallback: current working directory.
        return Directory.GetCurrentDirectory();
    }
}
