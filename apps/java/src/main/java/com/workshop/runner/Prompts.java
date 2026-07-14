package com.workshop.runner;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Reads the shared prompt manifests (minimal YAML) and renders {{var}} placeholders. */
public final class Prompts {
    private Prompts() {}

    private static final Pattern PLACEHOLDER = Pattern.compile("\\{\\{\\s*([a-z0-9_]+)\\s*\\}\\}");

    public static final class PromptException extends RuntimeException {
        public PromptException(String message) { super(message); }
    }

    public static final class Manifest {
        public String id = "", version = "", lab = "", variant = "", purpose = "";
        public String systemPrompt, userPrompt = "", outputSchema, testSet;
        public List<String> variables = new ArrayList<>();
        public File dir;
    }

    public static final class Rendered {
        public final String system;
        public final String user;
        public Rendered(String system, String user) { this.system = system; this.user = user; }
    }

    public static List<Manifest> iterManifests(File repoRoot) {
        List<Manifest> out = new ArrayList<>();
        File prompts = new File(repoRoot, "prompts");
        if (!prompts.isDirectory()) return out;
        collect(prompts, out);
        out.sort((a, b) -> a.id.compareTo(b.id));
        return out;
    }

    private static void collect(File dir, List<Manifest> out) {
        File[] files = dir.listFiles();
        if (files == null) return;
        for (File f : files) {
            if (f.isDirectory()) collect(f, out);
            else if (f.getName().endsWith(".manifest.yaml")) {
                try { out.add(loadManifest(f)); } catch (RuntimeException ignored) { /* skip malformed */ }
            }
        }
    }

    public static Manifest loadManifest(File path) {
        if (!path.isFile()) throw new PromptException("Manifest not found: " + path);
        List<String> lines;
        try { lines = Files.readAllLines(path.toPath()); }
        catch (IOException e) { throw new PromptException("Cannot read manifest: " + path); }

        Manifest m = new Manifest();
        m.dir = path.getAbsoluteFile().getParentFile();
        boolean inVariables = false;
        for (String raw : lines) {
            String line = stripComment(raw);
            if (line.isBlank()) continue;
            if (inVariables) {
                Matcher item = Pattern.compile("^\\s+-\\s+(.+?)\\s*$").matcher(line);
                if (item.matches()) { m.variables.add(unquote(item.group(1))); continue; }
                inVariables = false;
            }
            // top-level key: value
            Matcher kv = Pattern.compile("^([a-z_]+):\\s*(.*)$").matcher(line);
            if (kv.matches()) {
                String key = kv.group(1);
                String val = unquote(kv.group(2).trim());
                switch (key) {
                    case "id": m.id = val; break;
                    case "version": m.version = val; break;
                    case "lab": m.lab = val; break;
                    case "variant": m.variant = val; break;
                    case "purpose": m.purpose = val; break;
                    case "system_prompt": m.systemPrompt = val; break;
                    case "user_prompt": m.userPrompt = val; break;
                    case "output_schema": m.outputSchema = val; break;
                    case "test_set": m.testSet = val; break;
                    case "variables": inVariables = true; break;
                    default: /* ignore model/known_limitations/etc. */ break;
                }
            }
        }
        return m;
    }

    private static String stripComment(String line) {
        // Only strip full-line comments; keep '#' inside values rare in our manifests.
        String trimmed = line.stripLeading();
        if (trimmed.startsWith("#")) return "";
        return line;
    }

    private static String unquote(String v) {
        if (v.length() >= 2 && ((v.startsWith("\"") && v.endsWith("\"")) || (v.startsWith("'") && v.endsWith("'"))))
            return v.substring(1, v.length() - 1);
        return v;
    }

    public static String render(String template, Map<String, String> values, List<String> declared) {
        Matcher m = PLACEHOLDER.matcher(template);
        StringBuilder sb = new StringBuilder();
        while (m.find()) {
            String name = m.group(1);
            if (!declared.contains(name)) throw new PromptException("Prompt uses undeclared variable(s): " + name);
            if (!values.containsKey(name)) throw new PromptException("Missing value for variable: " + name);
            m.appendReplacement(sb, Matcher.quoteReplacement(values.get(name)));
        }
        m.appendTail(sb);
        return sb.toString();
    }

    public static Rendered build(Manifest manifest, Map<String, String> values) {
        String system = manifest.systemPrompt == null ? null
            : render(read(manifest.dir, manifest.systemPrompt), values, manifest.variables);
        String user = render(read(manifest.dir, manifest.userPrompt), values, manifest.variables);
        return new Rendered(system, user);
    }

    private static String read(File dir, String rel) {
        File fp = new File(dir, rel);
        if (!fp.isFile()) throw new PromptException("Referenced prompt file not found: " + fp);
        try { return Files.readString(fp.toPath()); }
        catch (IOException e) { throw new PromptException("Cannot read prompt file: " + fp); }
    }
}
