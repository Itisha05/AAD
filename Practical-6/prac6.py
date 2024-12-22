from flask import Flask, render_template, request

app = Flask(__name__)

def matrix_chain_order(p):
    n = len(p) - 1
    m = [[0 for _ in range(n)] for _ in range(n)]
    s = [[0 for _ in range(n)] for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    return m, s

def construct_optimal_solution(s, i, j):
    if i == j:
        return f"A{i + 1}"
    else:
        k = s[i][j]
        left = construct_optimal_solution(s, i, k)
        right = construct_optimal_solution(s, k + 1, j)
        return f"({left} x {right})"

@app.route('/', methods=['GET', 'POST'])
def index():
    num_matrices = None
    min_operations = None
    parenthesization = None
    m = None

    if request.method == 'POST':
        dimensions = list(map(int, request.form['dimensions'].split(',')))
        num_matrices = len(dimensions) - 1
        m, s = matrix_chain_order(dimensions)
        parenthesization = construct_optimal_solution(s, 0, len(dimensions) - 2)
        min_operations = m[0][-1]

       
        m = [['X' if cell == 0 else cell for cell in row] for row in m]

    return render_template('index.html', 
                           min_operations=min_operations, 
                           parenthesization=parenthesization, 
                           m=m, 
                           num_matrices=num_matrices)

if __name__ == '__main__':
    app.run(debug=True)

