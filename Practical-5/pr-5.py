from flask import Flask, render_template 
import plotly.graph_objs as go 
import plotly.offline as pyo
 
app = Flask(__name__) 
 
def min_coins(coins, value): 
        dp = [float('inf')] * (value + 1) 
        dp[0] = 0 
 
        for i in range(1, value + 1): 
            for coin in coins: 
                if i >= coin: 
                    dp[i] = min(dp[i], dp[i-coin] + 1) 
        return dp[value] if dp[value] != float('inf') else -1 
 
@app.route('/')
def index():
    coins = [1, 4, 6] 
    target_value = 9 
    result = min_coins(coins, target_value) 
    values = list(range(1, 21)) 
    results = [min_coins(coins, value) for value in values] 
    trace = go.Scatter(x=values, y=results, mode='lines+markers', name='Min Coins') 
    layout = go.Layout( 
    title='Minimum Coins Required for Different Values', xaxis=dict(title='Value (Rs.)'), yaxis=dict(title='Number of Coins'))
    fig = go.Figure(data=[trace], layout=layout) 
    plot_html = pyo.plot(fig, output_type='div', include_plotlyjs=True) 
    return render_template('index.html', plot=plot_html, coins=coins, target_value=target_value, result=result) 

if __name__ == '__main__': 
    app.run(debug=True) 
