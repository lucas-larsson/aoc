data class Range(val start: Int, var end: Int)

fun main() {
    val merged = mutableListOf(Range(10, 20))
    val start = 15
    val end = 25

    // ❌ BAD: Multiple lookups (like Python without walrus)
    if (start <= merged.last().end + 1) {
        merged[merged.lastIndex] = Range(
            merged.last().start,
            maxOf(merged.last().end, end)
        )
    }

    // ✅ GOOD: Local variable (like Java)
    val last = merged.last()
    if (start <= last.end + 1) {
        merged[merged.lastIndex] = Range(last.start, maxOf(last.end, end))
    }

    // ✅ KOTLIN WAY 1: Using .also {} (similar to walrus!)
    // .also returns the object after executing a block
    if (start <= merged.last().also { println("Accessing once: $it") }.end + 1) {
        merged.last().also { last ->
            merged[merged.lastIndex] = Range(last.start, maxOf(last.end, end))
        }
    }

    // ✅ KOTLIN WAY 2: Using .let {} for transformation
    merged.last().let { last ->
        if (start <= last.end + 1) {
            merged[merged.lastIndex] = Range(last.start, maxOf(last.end, end))
        }
    }

    // ✅ KOTLIN WAY 3: Using run {} for multiple operations
    merged.last().run {
        if (start <= end + 1) {
            merged[merged.lastIndex] = Range(this.start, maxOf(this.end, end))
        }
    }

    // 🔥 KOTLIN WAY 4: Using apply {} for modification
    merged[merged.lastIndex] = merged.last().apply {
        if (start <= end + 1) {
            end = maxOf(end, end)
        }
    }

    // 🏆 MOST KOTLIN-IDIOMATIC: Destructuring + takeIf
    val (lastStart, lastEnd) = merged.last()
    if (start <= lastEnd + 1) {
        merged[merged.lastIndex] = Range(lastStart, maxOf(lastEnd, end))
    }

    // 💎 COMPETITIVE PROGRAMMING STYLE: Local val is clearest
    val l = merged.last()
    if (start <= l.end + 1) {
        merged[merged.lastIndex] = Range(l.start, maxOf(l.end, end))
    }
}