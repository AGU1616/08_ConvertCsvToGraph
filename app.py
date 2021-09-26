"""
参考：https://qiita.com/OgawaHideyuki/items/b4e0c4f134c94037fd4f
参考：https://dash.plotly.com/dash-core-components/rangeslider

参考：plotlyの詳細設定など
    https://data-analytics.fun/2021/07/02/plotly-layout/
参考：CSS
    https://fromkato.com/webdev/css/properties/vertical-align
"""

import pandas as pd 
import numpy as np   
import dash  
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go 
# import json 

import base64
import io

##########################
##  User definition     ##
##########################
COLNAME1_X1 = 'X1'
COLNAME1_Y1 = 'Y1'
COLNAME1_Z1 = 'Z1'
COLNAME2_COM = 'COM'
COLNAME2_FB = 'FB'

# デフォルトで読み込むcsvファイルのパス
DEFALT_CSV_FAILE_PATH = './test.csv'
# ヘッダーの行番号（0オリジン）。指定した行からデータが読み込まれ、それより上の行は無視される。
HEADER_ROW = [4, 5]
df = pd.read_csv(DEFALT_CSV_FAILE_PATH, header=HEADER_ROW)
# df = pd.read_csv(DEFALT_CSV_FAILE_PATH, skiprows=[0,2]) # 1行目と3行目をスキップする場合（2行目をヘッダーとする）

##########################
##  Main Process        ##
##########################
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # # Title and so on
    # html.H3('CSV File ⇒ Graph', style={
    #     'textAlign': 'center',
    # }),

    # File Upload
    dcc.Upload(
        id='upload_data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select .csv File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '0 auto'
        },
        # Allow multiple files to be uploaded
        #multiple=True
    ),
    html.Div(id='output_upload_data', style={'width':'100%'}),

    html.Div([
        # Graph #1
        html.Div([
            dcc.Graph(id = 'chart-main'),
            dcc.RangeSlider(
                id='slider-one',
                min=0,
                max=len(df),
                step=1,
                value=[0, len(df)]
            ),
        ], style={
            'display': 'inline-block',
            'width': '60%',
            'vertical-align': 'top',
        }),

        # Graph #2
        html.Div([
            dcc.Graph(id='chart-one'),
            dcc.Graph(id='chart-two'),
            dcc.Graph(id='chart-three'),
        ],style={
            'display': 'inline-block',
            'width': '39%',
            'vertical-align': 'top',
        })
    ]),

])

##########################
##  CallBack Functions  ##
##########################
# Graph #1
@app.callback(
    Output('chart-main', 'figure'),
    [Input('slider-one', 'value')]
)
def update_graph(selected_range):
    dff = df[selected_range[0]:selected_range[1]]
    dff_x1 = dff[COLNAME1_X1, COLNAME2_COM]
    dff_y1 = dff[COLNAME1_Y1, COLNAME2_COM]
    dff_z1 = dff[COLNAME1_Z1, COLNAME2_COM]
    dff_x1_fb = dff[COLNAME1_X1, COLNAME2_FB]
    dff_y1_fb = dff[COLNAME1_Y1, COLNAME2_FB]
    dff_z1_fb = dff[COLNAME1_Z1, COLNAME2_FB]

    return {
        'data': [
            go.Scatter3d(
                x = dff_x1,
                y = dff_y1,
                z = dff_z1,
                mode = 'lines', #'markers',
                name = 'Command',
            ),
            go.Scatter3d(
                x = dff_x1_fb,
                y = dff_y1_fb,
                z = dff_z1_fb,
                mode = 'lines', #'markers',
                name = 'Feed Back',
            ),
        ],
        'layout': {
            'title': dict(text='<b>3D Scatter of X, Y, Z', font=dict(size=26, color='grey'), xref='paper', x=0.15, y=0.88, xanchor='center'),
            'legend': dict(xanchor='left', yanchor='bottom', x=0.02, y=0.9, orientation='h', 
                            bgcolor="white", bordercolor="grey", borderwidth=1),
            'height': 800,
            'xaxis': {
                'title': 'X-axis',
                'range': [-2, 2],   # なぜか効かない
            },
            'yaxis': {
                'title': 'Y-axis',
                'range': [-2, 2],   # なぜか効かない
            },
            'zaxis': {
                'title': 'Z-axis',
                'range': [-2, 2],   # なぜか効かない
            },
        }
    }


##########################
##  CallBack Functions  ##
##########################
# Graph #2
def create_smallChart(dff_time, dff1, dff2, name):
    return {
        'data':[
            go.Scatter(
                x = dff_time,
                y = dff1,
                mode = 'lines', #'markers',
                name = 'Command',
            ),
            go.Scatter(
                x = dff_time,
                y = dff2,
                mode = 'lines', #'markers',
                name = 'Feed Back',
            )
        ],
        'layout':{
            'title': dict(text='{}-Axis'.format(name), font=dict(size=26, color='grey'), xref='paper', x=0.08, y=0.88, xanchor='center'),
            'legend': dict(xanchor='left', yanchor='bottom', x=0.25, y=1.35, orientation='h', 
                            bgcolor="white", bordercolor="grey", borderwidth=1),
            'height': 300,
            'hovermode': 'x'
        }
    }

@app.callback(
    Output('chart-one', 'figure'),
    [Input('slider-one', 'value')]
)
def create_chartX1(selected_range):
    dff = df[selected_range[0]:selected_range[1]]

    diff_time = dff.index
    dff_x1 = dff[COLNAME1_X1, COLNAME2_COM]
    dff_x1_fb = dff[COLNAME1_X1, COLNAME2_FB]

    return create_smallChart(diff_time, dff_x1, dff_x1_fb,'X1')

@app.callback(
    Output('chart-two', 'figure'),
    [Input('slider-one', 'value')]
)
def create_chartY1(selected_range):
    dff = df[selected_range[0]:selected_range[1]]

    diff_time = dff.index
    dff_y1 = dff[COLNAME1_Y1, COLNAME2_COM]
    dff_y1_fb = dff[COLNAME1_Y1, COLNAME2_FB]

    return create_smallChart(diff_time, dff_y1, dff_y1_fb,'Y1')

@app.callback(
    Output('chart-three', 'figure'),
    [Input('slider-one', 'value')]
)
def create_chartZ1(selected_range):
    dff = df[selected_range[0]:selected_range[1]]

    diff_time = dff.index
    dff_z1 = dff[COLNAME1_Z1, COLNAME2_COM]
    dff_z1_fb = dff[COLNAME1_Z1, COLNAME2_FB]

    return create_smallChart(diff_time, dff_z1, dff_z1_fb,'Z1')


##########################
##  CallBack Functions  ##
##########################
# File Upload
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=HEADER_ROW)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded), header=HEADER_ROW)
    except Exception as e:
        print(e)
        return html.Div([
            'File loading error!'
        ])

    return df

# @app.callback([Output('input_dropdown1', 'options'), Output('input_dropdown1', 'value'), Output('output_memory', 'data')],
#               [Input('upload_data', 'contents')],
#               [State('upload_data', 'filename')])
@app.callback(
    [Output('slider-one', 'value'), Output('output_upload_data', 'children')],
    [Input('upload_data', 'contents')],
    [State('upload_data', 'filename')]
)
def update_dropdown(contents, filename):
    # ファイルがアップロードされるまでは、デフォルトファイルのグラフを表示するようにしたため、以下の例外処理をコメントアウト
    # コールバックが起こるがまだデータはアップロードされていないので、例外処理を行う
    # if contents is None:
    #     raise dash.exceptions.PreventUpdate

    global df   # グローバル変数のdfを書き換える(場合によっては、 dcc.Storeを使用することも検討)

    # ファイルがアップロードされるまでは、デフォルトファイルのグラフを表示する。
    if contents is not None:
        df = parse_contents(contents, filename)

    selected_range = [0, len(df)]
    return selected_range, filename


if __name__=="__main__":
    app.run_server(debug=True)