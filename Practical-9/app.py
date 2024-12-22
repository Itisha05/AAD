from flask import Flask, render_template, request 
app = Flask(__name__) 
def fractional_knapsack(profits, weights, max_weight): 
    items = [(profits[i] / weights[i], weights[i], profits[i]) for i in range(len(profits))] 
    items.sort(reverse=True, key=lambda x: x[0]) 
    total_profit = 0.0 
    remaining_weight = max_weight 
    fractions = [0] * len(profits) 
 
    for i in range(len(items)): 
        if remaining_weight >= items[i][1]: 
            total_profit += items[i][2] 
            remaining_weight -= items[i][1] 
            fractions[i] = 1 
        else: 
            fraction = remaining_weight / items[i][1] 
            total_profit += items[i][2] * fraction 
            fractions[i] = fraction 
            break 
 
    return items, fractions, total_profit 
 
@app.route('/', methods=['GET', 'POST']) 
def index(): 
    if request.method == 'POST': 
        profits = list(map(int, request.form['profits'].split(','))) 
        weights = list(map(int, request.form['weights'].split(','))) 
        max_weight = int(request.form['maxWeight']) 
 
        items, fractions, total_profit = fractional_knapsack(profits, weights, 
max_weight) 
 
        return render_template('index.html', items=items, fractions=fractions, 
total_profit=total_profit) 
 
    return render_template('index.html') 
 
if __name__ == '__main__': 
    app.run(debug=True)