from flask import Flask, render_template, request
import time
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

app = Flask(__name__)

employees = [
    {"id": 1, "name": "Mansi", "salary": 63000, "age": 55, "mobile": "9876543210", "designation": "Analyst"},
    {"id": 2, "name": "Princy", "salary": 66000, "age": 27, "mobile": "8765432109", "designation": "Senior Developer"},
    {"id": 3, "name": "Itisha", "salary": 80000, "age": 20, "mobile": "8394632754", "designation": "Project Manager"},
    {"id": 4, "name": "Trishla", "salary": 50000, "age": 40, "mobile": "6543210987", "designation": "Product Manager"},
    {"id": 5, "name": "Vaidehi", "salary": 46000, "age": 50, "mobile": "5432109876", "designation": "Marketing Manager"}
    
]

def linear_search(employees, key, value):
    start_time = time.time()
    for idx, emp in enumerate(employees):
        if emp[key] == value:
            time_taken = time.time() - start_time
            return emp, time_taken, idx + 1
    time_taken = time.time() - start_time
    return None, time_taken, len(employees)

def binary_search(employees, key, value, low, high, iterations=0):
    if low <= high:
        mid = (low + high) // 2
        iterations += 1
        if employees[mid][key] == value:
            return employees[mid], iterations
        elif employees[mid][key] < value:
            return binary_search(employees, key, value, mid + 1, high, iterations)
        else:
            return binary_search(employees, key, value, low, mid - 1, iterations)
    return None, iterations

def measure_time_binary_search(employees, key, value):
    start_time = time.time()
    result, iterations = binary_search(employees, key, value, 0, len(employees) - 1)
    time_taken = time.time() - start_time
    return result, time_taken, iterations

def plot_linear_graph(n_values, times, label, color):
    plt.figure(figsize=(5, 5))

    if len(n_values) >= 4:
        try:
            x_smooth = np.linspace(min(n_values), max(n_values), 300)
        except ValueError as e:
            print(f"Error with cubic spline interpolation: {e}")
            x_smooth = np.linspace(min(n_values), max(n_values), 300)
    else:
        x_smooth = np.linspace(min(n_values), max(n_values), 300)

    plt.plot(x_smooth, label=label, marker='', linewidth=4, color=color)
    plt.xlabel("Number of Elements (n)")
    plt.ylabel("Time Taken (seconds)")
    plt.legend()
    plt.title(f"{label} Time Complexity")
    plt.xlim(0, max(n_values) + 1)
    plt.ylim(0, max(times) + 0.1)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

def plot_smooth_binary_graph(n_values, times, label, color):
    plt.figure(figsize=(5, 5))

    if len(n_values) >= 4:
        try:
            x_smooth = np.linspace(min(n_values), max(n_values), 300)
        except ValueError as e:
            print(f"Error with cubic spline interpolation: {e}")
            x_smooth = np.linspace(min(n_values), max(n_values), 300)
    else:
        x_smooth = np.linspace(min(n_values), max(n_values), 300)

    plt.plot(x_smooth, label=label, marker='', linewidth=2, color=color)
    plt.xlabel("Number of Elements (n)")
    plt.ylabel("Time Taken (seconds)")
    plt.legend()
    plt.title(f"{label} Time Complexity")
    plt.xlim(0, max(n_values) + 1)
    plt.ylim(0, max(times) + 0.1)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        key = request.form['key']
        value = request.form['value']

        if key in ['id', 'salary', 'age']:
            value = int(value)

        linear_result, linear_time, linear_iterations = linear_search(employees, key, value)

        sorted_employees = sorted(employees, key=lambda x: x[key])
        binary_result, binary_time, binary_iterations = measure_time_binary_search(sorted_employees, key, value)

        n_values = list(range(0, len(employees) + 1))  

        linear_times = [(linear_iterations / len(employees)) * linear_time for _ in n_values]

        binary_times = [(binary_iterations / len(employees)) * np.log2(n) if n > 0 else 0 for n in n_values]

        linear_graph_url = plot_linear_graph(n_values, linear_times, "Linear Search (O(n))", 'red')
        binary_graph_url = plot_smooth_binary_graph(n_values, binary_times, "Binary Search (O(log n))", 'blue')

        return render_template('index.html', linear_result=linear_result, binary_result=binary_result,
                               linear_graph_url=linear_graph_url, binary_graph_url=binary_graph_url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

