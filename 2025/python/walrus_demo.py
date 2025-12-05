import time

# Create a list with lots of elements
merged = [(i, i+100) for i in range(1000)]

# Simulate the original approach
def without_walrus(iterations):
    count = 0
    for _ in range(iterations):
        # Access merged[-1] multiple times
        if merged[-1][1] > 0:
            count += merged[-1][0] + merged[-1][1]
    return count

# Simulate the walrus approach
def with_walrus(iterations):
    count = 0
    for _ in range(iterations):
        # Access merged[-1] once, then reuse
        if (last := merged[-1])[1] > 0:
            count += last[0] + last[1]
    return count

# Time them
iterations = 1_000_000_00

start = time.perf_counter()
result1 = without_walrus(iterations)
time1 = time.perf_counter() - start

start = time.perf_counter()
result2 = with_walrus(iterations)
time2 = time.perf_counter() - start

print(f"Without walrus: {time1*1000:.3f} ms")
print(f"With walrus:    {time2*1000:.3f} ms")
print(f"Speedup:        {time1/time2:.2f}x")
print(f"\nBoth produce same result: {result1 == result2}")