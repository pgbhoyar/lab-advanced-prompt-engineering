package com.workshop.runner;

import java.io.File;

/** Locates the repository root holding the shared prompts/, schemas/, datasets/. */
public final class RepoRoot {
    private RepoRoot() {}

    public static File find() {
        String env = System.getenv("WORKSHOP_REPO_ROOT");
        if (env != null && !env.isBlank()) return new File(env);

        File dir = new File(System.getProperty("user.dir"));
        while (dir != null) {
            if (new File(dir, "prompts").isDirectory() && new File(dir, "schemas").isDirectory()) {
                return dir;
            }
            dir = dir.getParentFile();
        }
        return new File(System.getProperty("user.dir"));
    }
}
