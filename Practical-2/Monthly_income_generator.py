import time 
import matplotlib.pyplot as plt 
import sys 
sys.setrecursionlimit(1000000) 

def sum_using_loop(N): 
    total = 0 
    for i in range(1, N + 1): 
        total += i
    return total 
 
def sum_using_equation(N): 
    return N * (N + 1) // 2 
 
def sum_using_recursion(N): 
    if N == 1: 
        return 1 
    return N + sum_using_recursion(N - 1) 
 
def measure_time(func, N): 
    start_time = time.time() 
    try: 
        func(N) 
    except RecursionError: 
        return float('inf') 
    end_time = time.time() 
    return end_time - start_time 
 
input_sizes = [100, 1000, 5000, 10000, 20000, 50000, 100000] 
loop_times = [] 
equation_times = [] 
recursion_times = [] 
 
for size in input_sizes: 
    loop_times.append(measure_time(sum_using_loop, size)) 
    equation_times.append(measure_time(sum_using_equation, size)) 
    recursion_times.append(measure_time(sum_using_recursion, size)) 
 
plt.figure(figsize=(12, 6)) 
plt.plot(input_sizes, loop_times, label='Loop', marker='o') 
plt.plot(input_sizes, equation_times, label='Equation', marker='o') 
plt.plot(input_sizes, recursion_times, label='Recursion', marker='o') 
plt.xlabel('Input Size (N)') 
plt.ylabel('Execution Time (seconds)') 
plt.title('Comparison of Execution Time for Sum of 1 to N') 
plt.legend() 
plt.grid(True) 
plt.show()
