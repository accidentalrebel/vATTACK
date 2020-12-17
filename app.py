from flask import Flask, render_template
import plotly.express as px
import json

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])

    div = fig.to_html(full_html=False)
    
    return div
