from flask import Flask, render_template, request, redirect, url_for 
import itertools 
import numpy as np 
app =Flask(__name__) 
def calculate_tsp(matrix): 
    n=len(matrix) 
    min_cost = float('inf') 
    min_path = [] 
     
    for perm in itertools.permutations(range(1, n)): 
        current_cost = matrix[0][perm[0]] + sum(matrix[perm[i]][perm[i+1]] for i in range(len(perm)- 1)) + matrix[perm[-1]][0] 
         
        if current_cost < min_cost: 
            min_cost = current_cost 
            min_path = [0] + list(perm) + [0] 
     
    path_taken = '- '.join(str(x + 1) for x in min_path) 
    min_cost_details = [(min_path[i] + 1, min_path[i + 1] + 1, matrix[min_path[i]][min_path[i + 1]]) for i in 
    range(len(min_path)- 1)] 
    return min_cost, path_taken, min_cost_details 
 
@app.route('/', methods=['GET', 'POST']) 
 
def input_matrix(): 
    if request.method == 'POST': 
        size = int(request.form['size']) 
        return redirect(url_for('get_matrix', size=size)) 
    return render_template('index3.html') 
 
@app.route('/matrix/<int:size>', methods=['GET', 'POST']) 
 
def get_matrix(size): 
    if request.method == 'POST': 
        matrix = [] 
        for i in range(size): 
            row =[] 
            for j in range(size): 
                value = request.form.get(f'cell_{i}_{j}') 
                row.append(float('inf') if value.lower() == 'inf' else int(value)) 
            matrix.append(row) 
        matrix = np.array(matrix) 
        min_cost, path_taken, min_cost_details = calculate_tsp(matrix) 
        return render_template('index1.html', min_cost=min_cost, path_taken=path_taken, 
min_cost_details=min_cost_details) 
    return render_template('index2.html', size=size) 
 
if __name__ == '__main__': 
    app.run(debug=True)