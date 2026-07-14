package com.workshop.runner;

import java.io.File;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * CLI entrypoint. Commands: check-config, list-labs, list-cases, run, validate.
 * Exit codes: 0 ok | 1 usage | 2 config | 3 model | 4 validation.
 */
public final class Main {
    private static final int OK = 0, USAGE = 1, CONFIG = 2, MODEL = 3, VALIDATION = 4;

    public static void main(String[] args) {
        System.exit(run(args));
    }

    static int run(String[] args) {
        if (args.length == 0) { System.err.println("Usage: <command> [options]"); return USAGE; }
        String cmd = args[0];
        Map<String, String> o = parseOptions(args);
        try {
            switch (cmd) {
                case "check-config": return checkConfig();
                case "list-labs": return listLabs();
                case "list-cases": return listCases(o);
                case "run": return runLab(o);
                case "validate": return validate(o);
                default: System.err.println("Unknown command: " + cmd); return USAGE;
            }
        } catch (Config.ConfigException e) {
            System.err.println("Config error: " + e.getMessage());
            return CONFIG;
        }
    }

    private static Map<String, String> parseOptions(String[] args) {
        Map<String, String> d = new HashMap<>();
        for (int i = 1; i < args.length; i++) {
            if (args[i].startsWith("--")) {
                String key = args[i].substring(2);
                if (i + 1 < args.length && !args[i + 1].startsWith("--")) d.put(key, args[++i]);
                else d.put(key, "true");
            }
        }
        return d;
    }

    private static int checkConfig() {
        Config cfg = Config.load(null);
        System.out.println("Config OK: " + cfg.redacted());
        return OK;
    }

    private static int listLabs() {
        File root = RepoRoot.find();
        Prompts.iterManifests(root).stream().map(m -> m.lab).distinct().sorted()
            .forEach(System.out::println);
        return OK;
    }

    private static int listCases(Map<String, String> o) {
        String lab = o.get("lab");
        if (lab == null) { System.err.println("--lab is required"); return USAGE; }
        File root = RepoRoot.find();
        List<Prompts.Manifest> manifests = Prompts.iterManifests(root).stream().filter(m -> m.lab.equals(lab)).toList();
        Prompts.Manifest withSet = manifests.stream().filter(m -> m.testSet != null).findFirst().orElse(null);
        if (withSet == null) { System.err.println("No test_set for lab '" + lab + "'."); return USAGE; }
        for (Cases.TestCase c : Cases.load(new File(withSet.dir, withSet.testSet)))
            System.out.println(c.id + "\t" + c.scenarioType);
        return OK;
    }

    private static int runLab(Map<String, String> o) {
        String lab = o.get("lab"), caseId = o.get("case"), variant = o.get("variant");
        if (lab == null || caseId == null || variant == null) {
            System.err.println("--lab, --case, and --variant are required"); return USAGE;
        }
        Config cfg = Config.load(null);
        File root = RepoRoot.find();
        Prompts.Manifest manifest = Prompts.iterManifests(root).stream()
            .filter(m -> m.lab.equals(lab) && m.variant.equals(variant)).findFirst().orElse(null);
        if (manifest == null) { System.err.println("No manifest for lab '" + lab + "' variant '" + variant + "'."); return USAGE; }
        if (manifest.testSet == null) { System.err.println("Manifest " + manifest.id + " has no test_set."); return USAGE; }

        Cases.TestCase testCase = Cases.find(new File(manifest.dir, manifest.testSet), caseId);
        Prompts.Rendered prompt = Prompts.build(manifest, testCase.input);

        System.out.println("Lab=" + manifest.lab + " case=" + testCase.id + " variant=" + manifest.variant
            + " prompt=" + manifest.id + "@" + manifest.version);
        if (!o.containsKey("quiet")) {
            if (prompt.system != null) System.out.println("\n--- SYSTEM ---\n" + prompt.system);
            System.out.println("\n--- USER ---\n" + prompt.user);
        }

        Object schema = null;
        if (manifest.outputSchema != null) {
            try { schema = Json.parse(Files.readString(new File(manifest.dir, manifest.outputSchema).toPath())); }
            catch (Exception e) { System.err.println("Cannot read schema: " + e.getMessage()); return USAGE; }
        }

        ModelClient client = new ModelClient(cfg, null);
        ModelClient.Response resp;
        try { resp = client.respond(prompt.system, prompt.user, schema); }
        catch (ModelClient.ModelException e) { System.err.println("Model error: " + e.getMessage()); return MODEL; }

        System.out.println("\n--- RESPONSE ---\n" + resp.text);

        if (schema != null) {
            Validate.Result v = Validate.structured(resp.text);
            System.out.println("\n" + v.summaryLine());
            for (String err : v.errors) System.err.println("  - " + err);
            if (!v.passed) return VALIDATION;
        }
        return OK;
    }

    @SuppressWarnings("unchecked")
    private static int validate(Map<String, String> o) {
        String text;
        try {
            if (o.containsKey("file")) text = Files.readString(new File(o.get("file")).toPath());
            else text = new String(System.in.readAllBytes());
        } catch (Exception e) { System.err.println("Cannot read input: " + e.getMessage()); return USAGE; }

        try {
            Object parsed = Json.parse(text);
            if (parsed instanceof Map && ((Map<String, Object>) parsed).containsKey("parsed_output"))
                text = JsonWriter.write(((Map<String, Object>) parsed).get("parsed_output"));
        } catch (RuntimeException ignored) { /* validate as-is */ }

        Validate.Result v = Validate.structured(text);
        System.out.println(v.summaryLine());
        for (String err : v.errors) System.err.println("  - " + err);
        return v.passed ? OK : VALIDATION;
    }
}
