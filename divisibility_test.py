divisors = []
num_regions = 17
for x in range(33, 100):
    val = x*(x+1)/2/num_regions
    if int(val) == val:
        divisors.append(x)

print(divisors)

