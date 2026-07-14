package com.workshop.runner;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;

/** Strict validation of the triage output contract — mirrors the Python/C# validators. */
public final class Validate {
    private Validate() {}

    private static final String[] REQUIRED = {
        "request_id", "summary", "category", "urgency", "recommended_action",
        "missing_information", "evidence", "confidence", "needs_human_review"
    };
    private static final Map<String, Set<String>> ALLOWED = Map.of(
        "category", Set.of("access", "hardware", "software", "network", "security", "other"),
        "urgency", Set.of("low", "medium", "high", "critical"),
        "confidence", Set.of("low", "medium", "high")
    );

    public static final class Result {
        public final boolean passed;
        public final List<String> errors;
        public Result(boolean passed, List<String> errors) { this.passed = passed; this.errors = errors; }
        public String summaryLine() { return passed ? "VALIDATION: PASS" : "VALIDATION: FAIL"; }
    }

    @SuppressWarnings("unchecked")
    public static Result structured(String responseText) {
        List<String> errors = new ArrayList<>();
        Object parsed;
        try {
            parsed = Json.parse(responseText == null ? "" : responseText.trim());
        } catch (RuntimeException e) {
            errors.add("Response is not valid JSON: " + e.getMessage());
            return new Result(false, errors);
        }
        if (!(parsed instanceof Map)) {
            errors.add("Root of the response must be a JSON object.");
            return new Result(false, errors);
        }
        Map<String, Object> obj = (Map<String, Object>) parsed;

        for (String f : REQUIRED) if (!obj.containsKey(f)) errors.add("Missing required field: " + f);

        Set<String> requiredSet = Set.of(REQUIRED);
        for (String key : obj.keySet())
            if (!requiredSet.contains(key)) errors.add("Unexpected field not in contract: " + key);

        for (Map.Entry<String, Set<String>> e : ALLOWED.entrySet()) {
            Object v = obj.get(e.getKey());
            if (v instanceof String && !e.getValue().contains(v))
                errors.add("Field '" + e.getKey() + "' has invalid value '" + v + "'.");
        }
        for (String f : new String[]{"missing_information", "evidence"}) {
            Object v = obj.get(f);
            if (v != null && !(v instanceof List)) errors.add("Field '" + f + "' must be an array.");
        }
        Object nhr = obj.get("needs_human_review");
        if (nhr != null && !(nhr instanceof Boolean)) errors.add("Field 'needs_human_review' must be a boolean.");

        return new Result(errors.isEmpty(), errors);
    }
}
