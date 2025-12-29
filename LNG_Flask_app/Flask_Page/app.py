from flask import Flask, render_template
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd



'''This File creates the Flask site for displaying the data analysis'''

#%%
'''Evaluation data from predictionmodel.py'''
mae_model = 0.96
rmse_model = 1.18
mae_zero = 0.90
rmse_zero = 1.10

pred = pd.read_csv("ttf_pred.csv")
pred["Date"] = pd.to_datetime(pred['Date'])
pred = pred.set_index("Date").sort_index()


#%%
app = Flask(__name__)

@app.route("/")
def index():
    Base_data = pd.read_csv("Flask_base_data.csv")
    df = Base_data[['Date','Exports', 'TTF_High']]
    
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values("Date").set_index("Date")
    df = df.join(pred, how= "left")
    
    fig = make_subplots(specs=[[{"secondary_y" : True}]])
    fig.add_trace(
        go.Scatter(
            x = df.index,
            y = df['TTF_High'],
            mode = "lines",
            name = "TTF_High"
            ),
        secondary_y = False
        
        )
    fig.add_trace(
        go.Scatter(
            x = df.index,
            y = df['TTF_Change_Pred'],
            mode = "lines",
            name = "Prediction"
            
            ),
        secondary_y= False
        )
    fig.add_trace(
        go.Bar(
            x = df.index,
            y = df['Exports'],
            name = "Exports",
            opacity = 0.7
            ),
        secondary_y= True
        )

    fig.update_layout(
        title= "TTF + Exports (SabinePass 2024)",
        xaxis_title= "Date"
        )


    fig.update_yaxes(title_text= "TTF High", secondary_y= False)
    fig.update_yaxes(title_text= "Exports", secondary_y= True)
    
    graph_html = fig.to_html(full_html= False)
    
    return render_template(
        "index.html",
        title = "LNG Exports from sabine pass impact on TTF price",
        graph_html= graph_html,
        mae = mae_model,
        baseline_mae = mae_zero,
        rmse = rmse_model,
        baseline_rmse = rmse_zero,
        )

if __name__ == "__main__":
    app.run(debug=True, use_reloader = False)



















