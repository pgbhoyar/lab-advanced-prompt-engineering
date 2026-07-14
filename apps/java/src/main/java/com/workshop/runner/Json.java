package com.workshop.runner;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** A small, dependency-free JSON parser (java.base only). Returns Map/List/String/Boolean/Double/null. */
public final class Json {
    private final String s;
    private int i;

    private Json(String s) { this.s = s; }

    public static final class JsonException extends RuntimeException {
        public JsonException(String message) { super(message); }
    }

    public static Object parse(String text) {
        Json p = new Json(text);
        p.ws();
        Object v = p.value();
        p.ws();
        if (p.i < p.s.length()) throw new JsonException("Trailing characters after JSON value");
        return v;
    }

    private Object value() {
        if (i >= s.length()) throw new JsonException("Unexpected end of input");
        char c = s.charAt(i);
        switch (c) {
            case '{': return object();
            case '[': return array();
            case '"': return string();
            case 't': case 'f': return bool();
            case 'n': return nul();
            default: return number();
        }
    }

    private Map<String, Object> object() {
        Map<String, Object> m = new LinkedHashMap<>();
        expect('{'); ws();
        if (peek() == '}') { i++; return m; }
        while (true) {
            ws();
            String key = string();
            ws(); expect(':'); ws();
            m.put(key, value());
            ws();
            char c = next();
            if (c == '}') return m;
            if (c != ',') throw new JsonException("Expected ',' or '}' in object");
        }
    }

    private List<Object> array() {
        List<Object> list = new ArrayList<>();
        expect('['); ws();
        if (peek() == ']') { i++; return list; }
        while (true) {
            ws();
            list.add(value());
            ws();
            char c = next();
            if (c == ']') return list;
            if (c != ',') throw new JsonException("Expected ',' or ']' in array");
        }
    }

    private String string() {
        expect('"');
        StringBuilder sb = new StringBuilder();
        while (true) {
            if (i >= s.length()) throw new JsonException("Unterminated string");
            char c = s.charAt(i++);
            if (c == '"') return sb.toString();
            if (c == '\\') {
                char e = s.charAt(i++);
                switch (e) {
                    case '"': sb.append('"'); break;
                    case '\\': sb.append('\\'); break;
                    case '/': sb.append('/'); break;
                    case 'n': sb.append('\n'); break;
                    case 't': sb.append('\t'); break;
                    case 'r': sb.append('\r'); break;
                    case 'b': sb.append('\b'); break;
                    case 'f': sb.append('\f'); break;
                    case 'u': sb.append((char) Integer.parseInt(s.substring(i, i + 4), 16)); i += 4; break;
                    default: throw new JsonException("Invalid escape: \\" + e);
                }
            } else {
                sb.append(c);
            }
        }
    }

    private Object number() {
        int start = i;
        while (i < s.length() && "-+.eE0123456789".indexOf(s.charAt(i)) >= 0) i++;
        String num = s.substring(start, i);
        if (num.isEmpty()) throw new JsonException("Invalid value at position " + start);
        return Double.parseDouble(num);
    }

    private Boolean bool() {
        if (s.startsWith("true", i)) { i += 4; return Boolean.TRUE; }
        if (s.startsWith("false", i)) { i += 5; return Boolean.FALSE; }
        throw new JsonException("Invalid literal");
    }

    private Object nul() {
        if (s.startsWith("null", i)) { i += 4; return null; }
        throw new JsonException("Invalid literal");
    }

    private void ws() { while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++; }
    private char peek() { return i < s.length() ? s.charAt(i) : '\0'; }
    private char next() { return s.charAt(i++); }
    private void expect(char c) { if (peek() != c) throw new JsonException("Expected '" + c + "'"); i++; }
}
