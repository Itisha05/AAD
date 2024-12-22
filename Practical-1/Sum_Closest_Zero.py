arr = []

print("Input:",end=' ')
x=input().split()
for i in range(len(x)):
    arr.append(int(x[i]))

nums=[]
least=100

for i in range(len(arr)):
    for j in range(i+1,len(arr)):
        x = arr[i] + arr[j]
        x = abs(x)
        if least > x:
            least = x
            nums=[arr[i],arr[j]]
        elif least == x:
            nums.extend([arr[i],arr[j]])
            
print("\nNumbers:")
if len(nums) > 2:
    for i in range(0,len(nums),2):
        print(f'{nums[i]}, {nums[i+1]}')
else:
    print(f'{nums[0]}, {nums[1]}')
