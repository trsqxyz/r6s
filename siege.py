
#! usr/bin/python3
# -*- coding: utf-8 -*-
# https://github.com/trsqxyz/r6s

import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

import math
import random

def random_color():
    return "rgb({}, {}, {})".format(*[random.randint(0, 255) for _ in range(3)])

data_base = pd.read_csv("siege_y1s4.csv")
like_columns = data_base.columns[1:-3:2]
power_columns = data_base.columns[2:-2:2]

names = list(like_columns)

like_means = [data_base[n].mean() for n in like_columns]
power_means = [data_base[n].mean() for n in power_columns]
plots = [(l,p) for (l,p) in zip(like_means, power_means)]

trace = [
    go.Scatter(
        x = [plots[n][0]],
        y = [plots[n][1]],
        mode = "markers",
        name = names[n],
        marker = {
            "color": random_color(),
        }
    ) 
    for n in range(len(plots))
]
data = go.Data(trace)
layout = go.Layout(
    xaxis = {
        "range": [1, 10],
    },
    yaxis = {
        "range": [1,10],
    },
    width = 1400,
    height = 950,
)

# questionnaire's resalt
fig = go.Figure(data = data, layout = layout)
py.image.save_as(fig, filename="siege_y1s4_base.png")

layout = go.Layout(
    width = 1400,
    height = 950,
    title = "operator's point = √((like^2 + power^2)/2)",
)

# operators heatmap
operators_point = []
for (nl, np) in zip(like_columns, power_columns):
    operators_point.append(
        [math.sqrt(
            (l**2 + p**2)/2) for (l, p) in zip(data_base[nl], data_base[np]
        )]
    )
    operators_point[-1].sort()
else:
    operators_point.reverse()

trace = [
    go.Heatmap(
        x = [1, 10],
        y = names[::-1],
        z = operators_point,
        colorscale = "Greens",
    )
]

data = go.Data(trace)
fig = go.Figure(data = data, layout = layout)
py.image.save_as(fig, filename = "operator's_point.png")
