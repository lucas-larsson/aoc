import java.util.*;

public class WalrusJava {
    static class Range {
        int start, end;
        Range(int s, int e) { start = s; end = e; }
    }

    public static void main(String[] args) {
        List<Range> merged = new ArrayList<>();
        merged.add(new Range(10, 20));

        int start = 15;
        int end = 25;

        // ❌ BAD: Multiple lookups (like Python without walrus)
        if (start <= merged.get(merged.size() - 1).end + 1) {
            Range last = merged.get(merged.size() - 1);
            merged.set(merged.size() - 1,
                new Range(merged.get(merged.size() - 1).start,
                         Math.max(merged.get(merged.size() - 1).end, end)));
        }

        // ✅ GOOD: Store in local variable (Java best practice)
        Range last = merged.get(merged.size() - 1);
        if (start <= last.end + 1) {
            merged.set(merged.size() - 1,
                new Range(last.start, Math.max(last.end, end)));
        }

        // ⚠️ POSSIBLE but not recommended: Assignment in condition
        // (This works but is considered bad style in Java)
        Range temp;
        if (start <= (temp = merged.get(merged.size() - 1)).end + 1) {
            merged.set(merged.size() - 1,
                new Range(temp.start, Math.max(temp.end, end)));
        }
    }
}