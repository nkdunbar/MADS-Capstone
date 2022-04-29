import subprocess
import sys

# Install all packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "../requirements.txt"])

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import accuracy_score, make_scorer
from sklearn.compose import make_column_transformer

# Constant
STATE_DICT = {1:'Alabama',2:'Alaska',4:'Arizona', 5:'Arkansas',6:'California',8:'Colorado',9:'Connecticut',
              10:'Delaware', 11:'District of Columbia', 12:'Florida', 13:'Georgia', 15:'Hawaii', 16:'Idaho', 
              17:'Illinois', 18:'Indiana', 19:'Iowa', 20:'Kansas', 21:'Kentucky', 22:'Louisiana', 23:'Maine', 
              24:'Maryland', 25:'Massachusetts', 26:'Michigan', 27:'Minnesota', 28:'Mississippi', 29:'Missouri',
              30:'Montana', 31:'Nebraska', 32:'Nevada', 33:'New Hampshire', 34:'New Jersey', 35:'New Mexico', 
              36:'New York', 37:'North Carolina', 38:'North Dakota', 39:'Ohio', 40:'Oklahoma', 42:'Pennsylvania',
              44:'Rhode Island', 45:'South Carolina', 46:'South Dakota', 47:'Tennessee', 48:'Texas', 49:'Utah',
              50:'Vermont', 51:'Virginia', 55:'Wisconsin', 56:'Wyoming', 72:'Puerto Rico', 53: 'Washington'}

REASON_DICT = {1:'1 - Treatment Completed', 
               2:'2 - Dropped out of treatment', 
               3:'3 - Terminated by facility', 
               4:'4 - Transferred to another treatment/facility',
               5:'5 - Incarcerated',
               6:'6 - Death',
               7:'7 - Other'}


US_STATE_TO_ABBREV = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

def read_csv(path):
    return pd.read_csv(path)

def preprocess_df(df, features, scaler):
    """
    Normalize the features in the dataframe with a given scaler function.
    :param df: DataFrame
    :param features: List[String]
    :param scaler: A function from https://scikit-learn.org/stable/modules/classes.html#module-sklearn.preprocessing
    """
    df[features] = scaler.fit_transform(df[features])
    return df

def preprocess(df, columns_list, scaler_list, remainder='passthrough'):
    """
    Normalize the features in the dataframe with a given scaler function.
    :param df: DataFrame
    :param features: List[List[String]]
    :param scaler: A list of scaler functions from https://scikit-learn.org/stable/modules/classes.html#module-sklearn.preprocessing
    """
    if type(columns_list) != list:
        raise Exception('columns_list must be list of list')
    if type(scaler_list) != list:
        raise Exception('scaler_list must be list')
    if len(columns_list) != len(scaler_list):
        raise Exception(f'column_list length {len(columns_list)} is different from scaler_list length {len(scaler_list)}')
    ct = make_column_transformer(*zip(scaler_list, columns_list), remainder=remainder)
    return ct.fit_transform(df)

def unsupervised_model(df, X, model):
    """
    Run a unsupervised model from sklearn
    :param df: DataFrame
    :param X: List[String]
    :param y: String
    :param model: A model function from sklearn i.e. PCA()
    """
    result = model.fit(df[X])
    transformed = model.transform(df[X])
    return result, transformed

def supervised_model(df, X, y, model, scoring_method=accuracy_score):
    """
    Run a supervised model from sklearn, return the model, predicted_y and the score (accuracy by default)
    :param df: DataFrame
    :param X: List[String]
    :param y: String
    :param model: A model function from sklearn i.e. LogisticRegression()
    :param scoring_method: Evaluation method such as accuracy_score()
    """
    y_true = df[[y]]
    model = model.fit(df[X], y_true)
    y_predicted = model.predict(df[X])
    score = scoring_method(y_true, y_predicted)
    return model, y_predicted, score

def pca_scatter_plot(df, pc1, pc2, color, is_static=True):
    labels={
        pc1: "Principal Component 1",
        pc2: "Principal Component 2"
    }
    fig = px.scatter(df, 
                     x=pc1, 
                     y=pc2, 
                     color=df[color].astype(str), 
                     labels=labels,
                     title="2 component PCA")
    config = {'staticPlot': is_static}

    fig.show(config=config)
    
    
def bar_chart(x, y, x_label, y_label, is_static=True):
    labels={
        'x': x_label,
        'y': y_label
    }
    config = {'staticPlot': is_static}
    fig = px.bar(x=x, y=y, labels=labels)
    fig.show(config=config)
    
def map_chart(df, z, reason, color_bar_title, title, states='ALL', is_static=True):
    df = df[df['REASON'] == REASON_DICT[reason]]
    if states != 'ALL':
        df = df[df['STFIPS'].isin(states)]
    data = go.Choropleth(
        locations=df['STFIPS'],
        z=df[z],
        locationmode = 'USA-states',
        colorscale = 'Blues',
        colorbar_title = color_bar_title)
    fig = go.Figure(data)
    config = {'staticPlot': is_static}
    fig.update_layout(
        title_text = title,
        geo_scope='usa')
    fig.show(config=config)
