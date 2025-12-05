# Walrus Operator Equivalent: Python vs Java vs Kotlin

## The Problem: Avoiding Redundant Lookups

### Python with Walrus Operator `:=` (Python 3.8+)
```python
# ✅ BEST: Walrus operator
if start <= (last := merged[-1])[1] + 1:
    merged[-1] = (last[0], max(last[1], end))
```
**Advantages:**
- ✅ Inline assignment
- ✅ Concise and readable
- ✅ Perfect for competitive programming

---

## Java

### Java Approach 1: Local Variable (Recommended)
```java
Range last = merged.get(merged.size() - 1);
if (start <= last.end + 1) {
    merged.set(merged.size() - 1,
        new Range(last.start, Math.max(last.end, end)));
}
```
**Advantages:**
- ✅ Clear and explicit
- ✅ Idiomatic Java
- ✅ Good for readability

### Java Approach 2: Assignment in Condition (Not Recommended)
```java
Range temp;
if (start <= (temp = merged.get(merged.size() - 1)).end + 1) {
    merged.set(merged.size() - 1,
        new Range(temp.start, Math.max(temp.end, end)));
}
```
**Issues:**
- ⚠️ Considered bad style in Java
- ⚠️ Looks like a bug (= vs ==)
- ⚠️ Many style checkers will flag this

**Java doesn't have a true walrus operator equivalent.** Best practice is to use a local variable before the if statement.

---

## Kotlin

Kotlin has **multiple elegant ways** to handle this pattern:

### Kotlin Approach 1: Local Variable (Most Clear)
```kotlin
val last = merged.last()
if (start <= last.end + 1) {
    merged[merged.lastIndex] = Range(last.start, maxOf(last.end, end))
}
```
**Best for:** Readability and competitive programming

### Kotlin Approach 2: `.let {}` Scope Function
```kotlin
merged.last().let { last ->
    if (start <= last.end + 1) {
        merged[merged.lastIndex] = Range(last.start, maxOf(last.end, end))
    }
}
```
**Best for:** Chaining operations

### Kotlin Approach 3: `.also {}` Scope Function
```kotlin
if (start <= merged.last().also { last = it }.end + 1) {
    merged[merged.lastIndex] = Range(last.start, maxOf(last.end, end))
}
```
**Best for:** Side effects while returning the original value

### Kotlin Approach 4: `.run {}` Scope Function
```kotlin
merged.last().run {
    if (start <= end + 1) {  // 'this' is the last element
        merged[merged.lastIndex] = Range(this.start, maxOf(this.end, end))
    }
}
```
**Best for:** Multiple operations on the same object

### Kotlin Approach 5: Destructuring
```kotlin
val (s, e) = merged.last()
if (start <= e + 1) {
    merged[merged.lastIndex] = Range(s, maxOf(e, end))
}
```
**Best for:** When you need multiple fields

---

## Performance Comparison

| Language | Method | Performance | Readability |
|----------|--------|-------------|-------------|
| Python | Walrus `:=` | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ Good |
| Python | Local var | ⚡⚡ Slower | ⭐⭐⭐⭐⭐ Best |
| Java | Local var | ⚡⚡⚡ Fast | ⭐⭐⭐⭐⭐ Best |
| Java | Inline assign | ⚡⚡⚡ Fast | ⭐ Poor |
| Kotlin | Local var | ⚡⚡⚡ Fast | ⭐⭐⭐⭐⭐ Best |
| Kotlin | `.let {}` | ⚡⚡ Slower | ⭐⭐⭐⭐ Good |
| Kotlin | `.also {}` | ⚡⚡ Slower | ⭐⭐⭐ OK |

---

## Recommendations

### For Competitive Programming:
- **Python:** Use walrus operator `:=`
- **Java:** Use local variable before if
- **Kotlin:** Use local `val` (shortest: `val l = merged.last()`)

### For Production Code:
- **Python:** Local variable is more readable for others
- **Java:** Always use local variable
- **Kotlin:** Use scope functions (`.let`, `.also`, `.run`) for idiomatic code

### Example in Competitive Programming:

**Python (Best):**
```python
if x <= (l := a[-1])[1] + 1: a[-1] = (l[0], max(l[1], y))
```

**Java (Verbose but clear):**
```java
Range l = a.get(a.size()-1);
if (x <= l.end+1) a.set(a.size()-1, new Range(l.start, Math.max(l.end,y)));
```

**Kotlin (Concise):**
```kotlin
val l = a.last()
if (x <= l.end+1) a[a.lastIndex] = Range(l.start, maxOf(l.end, y))
```

---

## Summary

| Feature | Python | Java | Kotlin |
|---------|--------|------|--------|
| **Inline assignment** | ✅ `:=` | ❌ (bad style) | ⚠️ (scope functions) |
| **Readability** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Performance** | ⚡⚡⚡ | ⚡⚡⚡ | ⚡⚡⚡ |
| **Brevity** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |

**Winner for competitive programming: Python's walrus operator** due to its perfect balance of brevity and clarity!