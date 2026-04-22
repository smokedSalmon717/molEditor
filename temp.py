L = [96, 100, 80, 80, 79.1, 79.5, 96, 75.2, 82, 77.9, 95]
L.sort()
L.pop(0)
L.pop(0)
num = L.pop(0)*0.5
num += L.pop(0)*0.5
den = 100
while L != []:
    num += L.pop()
    den += 100

print(num/den)