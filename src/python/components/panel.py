import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


class panel:
    def __init__(self, panel_title, data_model, panel_content=html.Div()):
        self.title = panel_title
        self.content = panel_content
        self.data_reader = data_model

    def update_content(self, content):
        self.content = content

    def render(self):
        self.layout = html.Div(
            [
                dbc.Row(dbc.Col(html.H1(self.title, className="panel_title"))),
                dbc.Row(self.content),
            ]
        )
        return self.layout

    @classmethod
    def create_card(cls, card_title, card_content, content_id):
        """create a dbc.Card object with title and content

        Args:
            card_title (string): title
            card_content (string): short content

        Returns:
            dbc.Card: card object
        """
        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H5(card_title, className="card-title"),
                    html.P(card_content, className="card-text", id=content_id),
                ]
            )
        )
        return card
