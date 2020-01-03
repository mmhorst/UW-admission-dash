#!/usr/bin/env python
# coding: utf-8

# In[1]:


import jupyter_plotly_dash, plotly, dash, sys, glob
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from jupyter_plotly_dash import JupyterDash


# In[2]:


path = sys.argv[1]


# In[3]:


def get_dfs(path):
    files = glob.glob(path+"*.csv")
    dfs = []
    for f in files:
        dfs.append(pd.read_csv(f))
    return dfs


# In[4]:


def get_years():
    years = [x for x in range(2011,2019)]
    return years


# In[5]:


def get_schools(dfs):
    schools = list(dfs[0]['UW School'])
    school_options = []
    for s in schools:
        school_options.append({'label':s, 'value':s})
    return school_options


# In[6]:


def get_groups(): 
    groups = "Total Female International Minority".split()
    group_options = []
    for group in groups:
        group_options.append({'label':group, 'value':group})
    return group_options


# In[7]:


def get_data(dfs, group, school):
    ydata = []
    for i in range(len(dfs)):
        cur_df = dfs[i]
        datum = cur_df[cur_df['UW School']==school][group].iloc[0]   # gets cell of school at group
        ydata.append(datum)

    return ydata


# In[8]:


## Setting up
dfs = get_dfs(path)
school_options = get_schools(dfs)
group_options = get_groups()
years = get_years()

## main web app function
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='UW Admission Stats: 2010-2018'),

    html.Div(children='''
        Which schools within UW are seeing explosive growth over the past decade? Which face student decline? 
        Use the interactive dashboard to view trends these data.
    '''),
    
     html.Label('\n'),
    dcc.Dropdown(
        id = 'Schools',
        options=school_options,
        value=["Education - College of"],
        multi=True
    ),
        dcc.RadioItems(
        id = 'Groups',
        options=group_options,
        value='Total'
    ),
    dcc.Graph(id='raw-graph'), 
    dcc.Graph(id='accepted-graph')
])

@app.callback(
    [dash.dependencies.Output('raw-graph', 'figure'), dash.dependencies.Output('accepted-graph', 'figure')], 
    [dash.dependencies.Input('Schools', 'value'), dash.dependencies.Input('Groups', 'value')]
)
def update_graphs(selec1, group):
    
    # Get column name from group selection
    if "International" == group:
        gr = "Intl_Applied"
        offer = "Intl_Percent_Offered"
    else: 
        gr = group+"_Applied"
        offer = group+"_Percent_Offered"
    
    data_offer = []
    data = []
    schos = []   # schools
    
    for scho in selec1:
        data.append({'x' : years, 'y': get_data(dfs, gr, scho),'type': 'line', 'name': scho})
        data_offer.append({'x' : years, 'y': get_data(dfs, offer, scho),'type': 'line', 'name': scho})
        
        
    # make multiple figures from data and data_offer
    fig={
    'data': data,
    'layout': {
        'title': 'UW Applications',
        'xaxis': {
            'title' : 'Years'
        },
        'yaxis': {
            'title' : group + " Applications"
        }
    }}
    figg={
    'data': data_offer,
    'layout': {
        'title': 'UW Acceptance Rate',
        'xaxis': {
            'title' : 'Years'
        },
        'yaxis': {
            'title' : group + " Percent Admission"
        }
    }}

    return fig, figg


# In[9]:


app


# In[ ]:




