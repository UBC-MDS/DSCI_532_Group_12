import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)
app.layout = html.Div(
    [html.H1("My Dash App"), dcc.Slider(min=0, max=5, marks={0: "0", 5: "Five"})]
)

if __name__ == "__main__":
    app.run_server(debug=True)  # activate hot reloading
