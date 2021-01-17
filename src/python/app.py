import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)
app.layout = html.Div(
    [
        html.H1("Covid Data Portal"),
        html.Div(
            html.Table(
                [
                    html.Tr(
                        [
                            html.Td(html.Div([html.H1("Global")])),
                            html.Td(html.Div([html.H1("World Map")])),
                            html.Td(
                                html.Div(
                                    [
                                        html.H1("Country"),
                                    ]
                                ),
                            ),
                        ]
                    )
                ]
            )
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)  # activate hot reloading
