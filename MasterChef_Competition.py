chef1 = list(map(int, input().split()))
chef2 = list(map(int, input().split()))

chef1_points = 0
chef2_points = 0

for i in range(3):
    if chef1[i] > chef2[i]:
        chef1_points += 1
    elif chef1[i] < chef2[i]:
        chef2_points += 1
    else:
        chef1_points += 0
        chef2_points += 0

print([chef1_points, chef2_points])
