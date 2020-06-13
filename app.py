import time
import importlib

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import torch

from torchvision.utils import make_grid
from dash.dependencies import Input, Output, State

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from models.semisup_vae import REVAE

import utils.dash_reusable_components as drc
import utils.figures as figs

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server

saved_clicks = None
# general stuff
revae = REVAE()
data = torch.load('./data/celeba.pt')

np.random.seed(1)
torch.manual_seed(1)

batch = data[np.random.choice(data.size(0), 100)]
grid = make_grid(batch, nrow=10)

img = batch[0]
recon = revae.reconstruct_img(img.unsqueeze(0))[0].detach()
z = revae._z_prior_fn(*revae.encoder_z(img.unsqueeze(0))).sample()


app.layout = html.Div(
    children=[
        # .container class is fixed, .container.scalable is scalable
        html.Div(
            className="banner",
            children=[
                # Change App Name here
                html.Div(
                    className="container scalable",
                    children=[
                        # Change App Name here
                        html.H2(
                            id="banner-title",
                            children=[
                                html.A(
                                    "ReVae: Rethinking Semi-Supervised Learning",
                                    href="",
                                    style={
                                        "text-decoration": "none",
                                        "color": "inherit",
                                    },
                                )
                            ],
                        ),
                        html.A(
                            id="banner-logo",
                            children=[
                                html.Img(src=app.get_asset_url("neurips.png"))
                            ],
                            href="",
                        ),
                    ],
                )
            ],
        ),
        html.Div(
            id="body",
            className="container scalable",
            children=[
                html.Div(
                    id="app-container",
                    # className="row",
                    children=[
                        html.Div(
                            id="left-column0",
                            children=[
                                drc.Card(
                                    id="first-card",
                                    children=[
                                        html.Button(
                                            "Change picture",
                                            id="change_pic",
                                        ),
                                    ],
                                ),
                                drc.Card(
                                    id="button-card",
                                    children=[
                                        drc.NamedSlider(
                                            name="Arched_Eyebrows",
                                            id="slider1",
                                            min=revae.lims[0][0],
                                            max=revae.lims[0][1],
                                            value=z[0, 0].item(),
                                            step=0.01,
                                        ),
                                        drc.NamedSlider(
                                            name="Bags_Under_Eyes",
                                            id="slider2",
                                            min=revae.lims[1][0],
                                            max=revae.lims[1][1],
                                            value=z[0, 1].item(),
                                            step=0.01,
                                        ),
                                        drc.NamedSlider(
                                            name="Bangs",
                                            id="slider3",
                                            min=revae.lims[2][0],
                                            max=revae.lims[2][1],
                                            value=z[0, 2].item(),
                                            step=0.01,
                                        ),
                                        drc.NamedSlider(
                                            name="Black_Hair",
                                            id="slider4",
                                            min=revae.lims[3][0],
                                            max=revae.lims[3][1],
                                            value=z[0, 3].item(),
                                            step=0.01,
                                        ),
                                        drc.NamedSlider(
                                            name="Blond_Hair",
                                            id="slider5",
                                            min=revae.lims[4][0],
                                            max=revae.lims[4][1],
                                            value=z[0, 4].item(),
                                            step=0.01,
                                        ),
                                        drc.NamedSlider(
                                            name="Brown_Hair",
                                            id="slider6",
                                            min=revae.lims[5][0],
                                            max=revae.lims[5][1],
                                            value=z[0, 5].item(),
                                            step=0.01,
                                        ),
                                        drc.NamedSlider(
                                            name="Bushy_Eyebrows",
                                            id="slider7",
                                            min=revae.lims[6][0],
                                            max=revae.lims[6][1],
                                            value=z[0, 6].item(),
                                            step=0.01,
                                        ),
                                        drc.NamedSlider(
                                            name="Chubby",
                                            id="slider8",
                                            min=revae.lims[7][0],
                                            max=revae.lims[7][1],
                                            value=z[0, 7].item(),
                                            step=0.01,
                                        ),
                                    ],
                                ),
                            ]
                        ),
                        html.Div(
                            # className="three columns",
                            id="left-column",
                            children=[
                                drc.Card(
                                    id="button-card2",
                                    children=[
                                        drc.NamedSlider(
                                            name="Eyeglasses",
                                            id="slider9",
                                            min=revae.lims[8][0],
                                            max=revae.lims[8][1],
                                            value=z[0, 8].item(),
                                            step=0.01,
                                        ),
                                        drc.NamedSlider(
                                            name="Heavy_Makeup",
                                            id="slider10",
                                            min=revae.lims[9][0],
                                            max=revae.lims[9][1],
                                            value=z[0, 9].item(),
                                            step=0.01,
                                        ),
                                        drc.NamedSlider(
                                            name="Male",
                                            id="slider11",
                                            min=revae.lims[10][0],
                                            max=revae.lims[10][1],
                                            value=z[0, 10].item(),
                                            step=0.01,
                                        ), 
                                        drc.NamedSlider(
                                            name="No_Beard",
                                            id="slider12",
                                            min=revae.lims[11][0],
                                            max=revae.lims[11][1],
                                            value=z[0, 11].item(),
                                            step=0.01,
                                        ), 
                                        drc.NamedSlider(
                                            name="Pale_Skin",
                                            id="slider13",
                                            min=revae.lims[12][0],
                                            max=revae.lims[12][1],
                                            value=z[0, 12].item(),
                                            step=0.01,
                                        ),   
                                        drc.NamedSlider(
                                            name="Receding_Hairline",
                                            id="slider14",
                                            min=revae.lims[13][0],
                                            max=revae.lims[13][1],
                                            value=z[0, 13].item(),
                                            step=0.01,
                                        ),   
                                        drc.NamedSlider(
                                            name="Smiling",
                                            id="slider15",
                                            min=revae.lims[14][0],
                                            max=revae.lims[14][1],
                                            value=z[0, 14].item(),
                                            step=0.01,
                                        ),       
                                        drc.NamedSlider(
                                            name="Wavy_Hair",
                                            id="slider16",
                                            min=revae.lims[15][0],
                                            max=revae.lims[15][1],
                                            value=z[0, 15].item(),
                                            step=0.01,
                                        ),        
                                        drc.NamedSlider(
                                            name="Young",
                                            id="slider17",
                                            min=revae.lims[16][0],
                                            max=revae.lims[16][1],
                                            value=z[0, 16].item(),
                                            step=0.01,
                                        ),             
                                        #html.Button(
                                        #    "Reset Threshold",
                                        #    id="button-zero-threshold",
                                        #),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            id="div-graphs",
                            children=dcc.Graph(
                                id="graph-sklearn-svm",
                                figure=dict(
                                    layout=dict(
                                        plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                    )
                                ),
                            ),
                        ),
                    ],
                )
            ],
        ),
    ]
)

@app.callback(
    Output("div-graphs", "children"),
    [
        Input("change_pic", "n_clicks"),
        Input('slider1', 'value'),
        Input('slider2', 'value'),
        Input('slider3', 'value'),
        Input('slider4', 'value'),
        Input('slider5', 'value'),
        Input('slider6', 'value'),
        Input('slider7', 'value'),
        Input('slider8', 'value'),
        Input('slider9', 'value'),
        Input('slider10', 'value'),
        Input('slider11', 'value'),
        Input('slider12', 'value'),
        Input('slider13', 'value'),
        Input('slider14', 'value'),
        Input('slider15', 'value'),
        Input('slider16', 'value'),
        Input('slider17', 'value')
    ],
)
def update_svm_graph(
    n_clicks,
    slider1, slider2, slider3, slider4, slider5, slider6, slider7, slider8, 
    slider9, slider10, slider11, slider12, slider13, slider14, slider15, slider16, slider17,
):

    np.random.seed(1)
    torch.manual_seed(1)

    coords = 0

    if n_clicks:
 
        #batch = data[np.random.choice(data.size(0), 100)]
        #grid = make_grid(batch, nrow=10)

        coords = n_clicks
    
        #img = batch[(9 - int(coords[2])) * 10 + int(coords[0])]
        #recon = revae.reconstruct_img(img.unsqueeze(0))[0].detach()
        #z = revae._z_prior_fn(*revae.encoder_z(img.unsqueeze(0))).sample()
    
    #

    sliders = [slider1, slider2, slider3, slider4, slider5, slider6, slider7, slider8, 
    slider9, slider10, slider11, slider12, slider13, slider14, slider15, slider16, slider17]  

    batch = data[np.random.choice(data.size(0), 100)]
    grid = make_grid(batch, nrow=10)

    img = batch[coords]
    recon = revae.reconstruct_img(img.unsqueeze(0))[0].detach()
    z = revae._z_prior_fn(*revae.encoder_z(img.unsqueeze(0))).sample()
    z = revae._z_prior_fn(*revae.encoder_z(img.unsqueeze(0))).sample()

    for i, slider in enumerate(sliders):
        z[0, i] = torch.tensor([[slider]])
    with torch.no_grad():
        img = revae.decoder(z).squeeze()
        fig = px.imshow(img.permute(1, 2, 0))

    axis_template = dict(showgrid = False, zeroline = False,
            linecolor = 'black', showticklabels = False)
    fig.update_layout(height=600,xaxis=axis_template, yaxis = axis_template, plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd"},)

    return [
        html.Div(
            id="svm-graph-container",
            children=dcc.Loading(
                className="graph-wrapper",
                children=dcc.Graph(id="graph-sklearn-svm", figure=fig),
                style={"display": "none"},
            ),
        ),
    ]



# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)