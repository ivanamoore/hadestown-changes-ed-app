import pandas as pd
import numpy as np
import difflib


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

df = pd.read_csv('~/Hadestown.csv', sep = '$')
df.lyrics = [i.replace('\", ','\', ') for i in df.lyrics]
df.lyrics = [i.strip('][').split('\', ') for i in df.lyrics]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.layout = html.Div(children=[
    html.H1( id = 'title',
        children = 'Hadestown Concept -> Cast -> Broadway Changes'),
    html.H6(id = 'subtitle',
        children = 'This is a web-application that uses Genius provided lyrics and the difflib library to track the changes per song and per album! Enjoy! (This was made for educational purposes only.)'),

    html.Label('Choose a song'),

    dcc.Dropdown(id = 'Song',
        options=[
            {'label':'Wedding Song', 'value':0},
            {'label':'Epic I', 'value':1},
            {'label':'Way Down Hadestown I', 'value':2},
            {'label':'Hey, Little Songbird', 'value':3},
            {'label':'Gone, I\'m Gone', 'value':4},
            {'label':'When the Chips Are Down', 'value':5},
            {'label':'Wait for Me I', 'value':6},
            {'label':'Why We Build the Wall', 'value':7},
            {'label':'Our Lady of the Underground', 'value':8},
            {'label':'Flowers', 'value':9},
            {'label':'Nothing Changes', 'value':10},
            {'label':"If It's True", 'value':11},
            {'label':'Papers', 'value':12},
            {'label':'How Long?', 'value':13},
            {'label':'Epic II', 'value':14},
            {'label':"Lover's Desire", 'value':15},
            {'label':'His Kiss, the Riot', 'value':16},
            {'label':'Doubt Comes In', 'value':17},
            {'label':'I/We Raise My/Our Cup/s', 'value':18},
            {'label':'Any Way The Wind Blows', 'value':19},
            {'label':'Road to Hell', 'value':20},
            {'label':'Come Home With Me I', 'value':21},
            {'label':"Livin' It Up", 'value':22},
            {'label':"All I've Ever Known", 'value':23},
            {'label':'Chant I', 'value':24},
            {'label':'Way Down Hadestown II', 'value':25},
            {'label':'Come Home With Me II', 'value':26},
            {'label':'Chant II', 'value':27},
            {'label':'Epic III', 'value':28},
            {'label':'Word to the Wise', 'value':29},
            {'label':'Promises', 'value':30},
            {'label':'Wait for Me II', 'value':31},
            {'label':'Road to Hell II', 'value':32},
            {'label':'A Gathering Storm', 'value':33},


        ]),
    html.Label('Choose the First Album'),
   # dcc.RadioItems( id = 'Album1',
   #     options =[
   #         {'label':'Concept Album', 'value':'Hadestown'},
   #         {'label':'Cast Recording', 'value':'Hadestown: The Myth. The Musical. (Live Original Cast Recording)'},
   #         {'label':'Broadway Recording', 'value':'Hadestown (Original Broadway Cast Recording)'}
   #     ], value = 'Hadestown'),
    dcc.RadioItems(id = 'Album1'),
html.Div( children = [
    html.Label('Choose the Second Album'),
    dcc.RadioItems(id = 'Album2')]),
  #  dcc.RadioItems( id = 'Album2',
   #     options =[
    #        {'label':'Concept Album', 'value':'Hadestown'},
     #       {'label':'Cast Recording', 'value':'Hadestown: The Myth. The Musical. (Live Original Cast Recording)'},
      #      {'label':'Broadway Recording', 'value':'Hadestown (Original Broadway Cast Recording)'}
       # ], value = 'Hadestown'),
    html.Label('Pleast click submit below:'),
    html.Button(id = 'button', children = 'Submit', n_clicks=0),
    html.Hr(),
    html.Iframe(id = 'text', srcDoc='', style={'width':'90%', 'height':'500px', 'overflow':'auto'})

])

@app.callback(
    Output ('Album1','options'),
    [Input ('Song','value')])
def set_album1_output(selected_song):
    selected_song = int(selected_song)
    if selected_song in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18]:
        return [{'label':'Concept Album', 'value':'Hadestown'}, {'label':'Cast Recording', 'value':'Hadestown: The Myth. The Musical. (Live Original Cast Recording)'},{'label':'Broadway Recording', 'value':'Hadestown (Original Broadway Cast Recording)'}]
    elif selected_song in [19,20,21,22,23,24,25,26,27,28,29,30,31,32]:
        return [{'label':'Cast Recording', 'value':'Hadestown: The Myth. The Musical. (Live Original Cast Recording)'},{'label':'Broadway Recording', 'value':'Hadestown (Original Broadway Cast Recording)'}]
    elif selected_song in [15]:
        return [{'label':'Concept Album', 'value':'Hadestown'}]
    elif selected_song in [33]:
        return [{'label':'Broadway Recording', 'value':'Hadestown (Original Broadway Cast Recording)'}]

@app.callback(
    Output('Album1','value'),
    [Input('Album1','options')]
)

def album1_output(available_options):
    return available_options[0]['value']

@app.callback(
    Output ('Album2','options'),
    [Input ('Song','value')])

def set_album2_output(selected_song):
    selected_song = int(selected_song)
    if selected_song in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18]:
        return [{'label':'Concept Album', 'value':'Hadestown'}, {'label':'Cast Recording', 'value':'Hadestown: The Myth. The Musical. (Live Original Cast Recording)'},{'label':'Broadway Recording', 'value':'Hadestown (Original Broadway Cast Recording)'}]
    elif selected_song in [19,20,21,22,23,24,25,26,27,28,29,30,31,32]:
        return [{'label':'Cast Recording', 'value':'Hadestown: The Myth. The Musical. (Live Original Cast Recording)'},{'label':'Broadway Recording', 'value':'Hadestown (Original Broadway Cast Recording)'}]
    elif selected_song in [15]:
        return [{'label':'Concept Album', 'value':'Hadestown'}]
    elif selected_song in [33]:
        return [{'label':'Broadway Recording', 'value':'Hadestown (Original Broadway Cast Recording)'}]

@app.callback(
    Output('Album2','value'),
    [Input('Album2','options')]
)

def album2_output(available_options):
    return available_options[0]['value']



@app.callback (
    Output('text','srcDoc'), 
    [Input('button','n_clicks')],
    [State('Song','value'),
    State('Album1', 'value'),
    State('Album2','value')])

def show_comparison (button, Song, Album1, Album2):
    a = df[(df.album==str(Album1)) & (df.song_key==int(Song))]['lyrics'].values[0]
    b = df[(df.album==str(Album2)) & (df.song_key==int(Song))]['lyrics'].values[0]
    diff = difflib.HtmlDiff().make_file(a,b)
    return diff

if __name__ == '__main__':
    app.run_server(debug=False)
