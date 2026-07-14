package com.workshop.runner;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Loads .jsonl test sets using the dependency-free JSON parser. */
public final class Cases {
    private Cases() {}

    public static final class CaseException extends RuntimeException {
        public CaseException(String message) { super(message); }
    }

    public static final class TestCase {
        public final String id;
        public final String scenarioType;
        public final Map<String, String> input;
        public TestCase(String id, String scenarioType, Map<String, String> input) {
            this.id = id; this.scenarioType = scenarioType; this.input = input;
        }
    }

    @SuppressWarnings("unchecked")
    public static List<TestCase> load(File path) {
        if (!path.isFile()) throw new CaseException("Test set not found: " + path);
        List<TestCase> out = new ArrayList<>();
        List<String> lines;
        try { lines = Files.readAllLines(path.toPath()); }
        catch (IOException e) { throw new CaseException("Cannot read test set: " + path); }

        int lineNo = 0;
        for (String raw : lines) {
            lineNo++;
            String line = raw.trim();
            if (line.isEmpty()) continue;
            Object parsed;
            try { parsed = Json.parse(line); }
            catch (RuntimeException e) { throw new CaseException("Invalid JSON on line " + lineNo + " of " + path + ": " + e.getMessage()); }
            Map<String, Object> obj = (Map<String, Object>) parsed;
            Map<String, Object> inputRaw = (Map<String, Object>) obj.get("input");
            Map<String, String> input = new LinkedHashMap<>();
            for (Map.Entry<String, Object> e : inputRaw.entrySet())
                input.put(e.getKey(), String.valueOf(e.getValue()));
            out.add(new TestCase((String) obj.get("id"), (String) obj.get("scenario_type"), input));
        }
        return out;
    }

    public static TestCase find(File path, String caseId) {
        for (TestCase c : load(path)) if (c.id.equals(caseId)) return c;
        throw new CaseException("Test case '" + caseId + "' not found in " + path);
    }
}
