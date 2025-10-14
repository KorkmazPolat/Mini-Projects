
days = 365  

# --- Example for 3 students ---
p_no = 1.0
for k in range(3):
    p_no *= (days - k) / days  
p_not = 1 - p_no

print("For 3 students:")
print(f"  P(no shared birth:) = {p_no:.12f}")
print(f"  P(at least one shared birthday) = {p_not:.12f}\n")


# --- For-loop: probabilities for first 60 students ---
p_no = 1.0
print("n | P(no shared)         | P(at least one shared)")
print("-" * 55)
for n in range(1, 61):
    if n == 1:
        p_no = 1.0
    else:
        p_no *= (days - (n - 1)) / days
    p_not = 1 - p_no
    print(f"{n:2d} | {p_no:.12f} | {p_not:.12f}")


# --- While-loop: find the first n where probability > 0.5 ---
p_no = 1.0
n = 0
while True:
    n += 1
    if n == 1:
        p_no = 1.0
    else:
        p_no *= (days - (n - 1)) / days
    p_not = 1 - p_no
    if p_not > 0.5:
        print(f"\nThe probability first exceeds 0.5 at n = {n} (probability = {p_not:.12f})")
        break
