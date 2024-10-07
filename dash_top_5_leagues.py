from dash import Dash, dcc, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


app = Dash(__name__)


df = pd.read_csv('past-data.csv')

colunas = ['Season', 'Div', 'Time', 'HTHG', 'HTAG', 'HTR', 'Referee', 'HC', 'AC', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'HS', 'AS', 'HST', 'AST']

# Premier League
df_pl = df[(df['Season'] == '22-23') & (df['Div'] == 'Premier League')]
df_pl.reset_index(inplace=True)
df_pl.drop(df[colunas], axis=1, inplace=True)
df_pl.drop('index', axis=1, inplace=True)

wins_pl = []
draws_pl = []
loses_pl = []

for i in df_pl.index:
    if df_pl.iloc[i]['FTR'] == 'H':
        wins_pl.append(df_pl.iloc[i]['HomeTeam'])
        loses_pl.append(df_pl.iloc[i]['AwayTeam'])
    elif df_pl.iloc[i]['FTR'] == 'A':
        loses_pl.append(df_pl.iloc[i]['HomeTeam'])
        wins_pl.append(df_pl.iloc[i]['AwayTeam'])
    else:
        draws_pl.append(df_pl.iloc[i]['HomeTeam'])
        draws_pl.append(df_pl.iloc[i]['AwayTeam'])

wins_pl = pd.DataFrame(wins_pl, columns=['Team'])
draws_pl = pd.DataFrame(draws_pl, columns=['Team'])
loses_pl = pd.DataFrame(loses_pl, columns=['Team'])

wins_pl = wins_pl['Team'].value_counts().reset_index()
loses_pl = loses_pl['Team'].value_counts().reset_index()
draws_pl = draws_pl['Team'].value_counts().reset_index()

wins_pl.columns = ['Team', 'Count']
loses_pl.columns = ['Team', 'Count']
draws_pl.columns = ['Team', 'Count']

home_score_pl = df_pl.groupby('HomeTeam')['FTHG'].sum().sort_values(ascending=False).reset_index()
home_score_pl.columns = ['Team', 'Goals']
away_score_pl = df_pl.groupby('AwayTeam')['FTAG'].sum().sort_values(ascending=False).reset_index()
away_score_pl.columns = ['Team', 'Goals']
total_score_pl = pd.concat([home_score_pl, away_score_pl])
total_score_pl = total_score_pl.groupby('Team')['Goals'].sum().sort_values(ascending=False).reset_index()

df_pl['HomeWin'] = (df_pl['FTHG'] > df_pl['FTAG']).astype(int)
df_pl['AwayWin'] = (df_pl['FTHG'] < df_pl['FTAG']).astype(int)

df_pl['HomePoints'] = df_pl['HomeWin'] * 3
df_pl['AwayPoints'] = df_pl['AwayWin'] * 3
df_pl['DrawPoints'] = (df_pl['FTHG'] == df_pl['FTAG']).astype(int)

home_points_pl = df_pl.groupby('HomeTeam')['HomePoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'HomePoints': 'Points'})
away_points_pl = df_pl.groupby('AwayTeam')['AwayPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'AwayPoints': 'Points'})

draw_points_home_pl = df_pl.groupby('HomeTeam')['DrawPoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'DrawPoints': 'Points'})
draw_points_away_pl = df_pl.groupby('AwayTeam')['DrawPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'DrawPoints': 'Points'})
total_draw_points_pl = pd.concat([draw_points_home_pl, draw_points_away_pl]).groupby('Team').sum().reset_index()
total_points_pl = pd.concat([home_points_pl, away_points_pl, total_draw_points_pl]).groupby('Team').sum().reset_index()

total_points_pl = total_points_pl.sort_values(by='Points', ascending=False).reset_index()

table_pl = total_points_pl.drop('index', axis=1)

pos_pl = pd.DataFrame()

for date in df_pl['Date'].unique():
    current_matches_pl = df_pl[df_pl['Date'] <= date]
    home_points_pl = current_matches_pl.groupby('HomeTeam')['HomePoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'HomePoints': 'Points'})
    away_points_pl = current_matches_pl.groupby('AwayTeam')['AwayPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'AwayPoints': 'Points'})

    draw_points_home_pl = current_matches_pl.groupby('HomeTeam')['DrawPoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'DrawPoints': 'Points'})
    draw_points_away_pl = current_matches_pl.groupby('AwayTeam')['DrawPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'DrawPoints': 'Points'})
    
    total_draw_points_pl = pd.concat([draw_points_home_pl, draw_points_away_pl]).groupby('Team').sum().reset_index()
    
    total_points_pl = pd.concat([home_points_pl, away_points_pl, total_draw_points_pl]).groupby('Team').sum().reset_index()
    
    total_points_pl['Date'] = date
    total_points_pl['Positions'] = total_points_pl['Points'].rank(method='min', ascending=False)
    
    pos_pl = pd.concat([pos_pl, total_points_pl])

opcoes_pl = list(df_pl.HomeTeam.sort_values().unique())
opcoes_pl.append('Todos')


# LaLiga
df_ll = df[(df['Season'] == '22-23') & (df['Div'] == 'LaLiga')]
df_ll.reset_index(inplace=True)
df_ll.drop(df[colunas], axis=1, inplace=True)
df_ll.drop('index', axis=1, inplace=True)

wins_ll = []
draws_ll = []
loses_ll = []

for i in df_ll.index:
    if df_ll.iloc[i]['FTR'] == 'H':
        wins_ll.append(df_ll.iloc[i]['HomeTeam'])
        loses_ll.append(df_ll.iloc[i]['AwayTeam'])
    elif df_ll.iloc[i]['FTR'] == 'A':
        loses_ll.append(df_ll.iloc[i]['HomeTeam'])
        wins_ll.append(df_ll.iloc[i]['AwayTeam'])
    else:
        draws_ll.append(df_ll.iloc[i]['HomeTeam'])
        draws_ll.append(df_ll.iloc[i]['AwayTeam'])

wins_ll = pd.DataFrame(wins_ll, columns=['Team'])
draws_ll = pd.DataFrame(draws_ll, columns=['Team'])
loses_ll = pd.DataFrame(loses_ll, columns=['Team'])

wins_ll = wins_ll['Team'].value_counts().reset_index()
loses_ll = loses_ll['Team'].value_counts().reset_index()
draws_ll = draws_ll['Team'].value_counts().reset_index()

wins_ll.columns = ['Team', 'Count']
loses_ll.columns = ['Team', 'Count']
draws_ll.columns = ['Team', 'Count']

home_score_ll = df_ll.groupby('HomeTeam')['FTHG'].sum().sort_values(ascending=False).reset_index()
home_score_ll.columns = ['Team', 'Goals']
away_score_ll = df_ll.groupby('AwayTeam')['FTAG'].sum().sort_values(ascending=False).reset_index()
away_score_ll.columns = ['Team', 'Goals']
total_score_ll = pd.concat([home_score_ll, away_score_ll])
total_score_ll = total_score_ll.groupby('Team')['Goals'].sum().sort_values(ascending=False).reset_index()

df_ll['HomeWin'] = (df_ll['FTHG'] > df_ll['FTAG']).astype(int)
df_ll['AwayWin'] = (df_ll['FTHG'] < df_ll['FTAG']).astype(int)

df_ll['HomePoints'] = df_ll['HomeWin'] * 3
df_ll['AwayPoints'] = df_ll['AwayWin'] * 3
df_ll['DrawPoints'] = (df_ll['FTHG'] == df_ll['FTAG']).astype(int)

home_points_ll = df_ll.groupby('HomeTeam')['HomePoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'HomePoints': 'Points'})
away_points_ll = df_ll.groupby('AwayTeam')['AwayPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'AwayPoints': 'Points'})

draw_points_home_ll = df_ll.groupby('HomeTeam')['DrawPoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'DrawPoints': 'Points'})
draw_points_away_ll = df_ll.groupby('AwayTeam')['DrawPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'DrawPoints': 'Points'})
total_draw_points_ll = pd.concat([draw_points_home_ll, draw_points_away_ll]).groupby('Team').sum().reset_index()
total_points_ll = pd.concat([home_points_ll, away_points_ll, total_draw_points_ll]).groupby('Team').sum().reset_index()

total_points_ll = total_points_ll.sort_values(by='Points', ascending=False).reset_index()

table_ll = total_points_ll.drop('index', axis=1)

pos_ll = pd.DataFrame()

for date in df_ll['Date'].unique():
    current_matches_ll = df_ll[df_ll['Date'] <= date]
    home_points_ll = current_matches_ll.groupby('HomeTeam')['HomePoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'HomePoints': 'Points'})
    away_points_ll = current_matches_ll.groupby('AwayTeam')['AwayPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'AwayPoints': 'Points'})

    draw_points_home_ll = current_matches_ll.groupby('HomeTeam')['DrawPoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'DrawPoints': 'Points'})
    draw_points_away_ll = current_matches_ll.groupby('AwayTeam')['DrawPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'DrawPoints': 'Points'})
    
    total_draw_points_ll = pd.concat([draw_points_home_ll, draw_points_away_ll]).groupby('Team').sum().reset_index()
    
    total_points_ll = pd.concat([home_points_ll, away_points_ll, total_draw_points_ll]).groupby('Team').sum().reset_index()
    
    total_points_ll['Date'] = date
    total_points_ll['Positions'] = total_points_ll['Points'].rank(method='min', ascending=False)
    
    pos_ll = pd.concat([pos_ll, total_points_ll])

opcoes_ll = list(df_ll.HomeTeam.sort_values().unique())
opcoes_ll.append('Todos')


# Bundesliga
df_bl = df[(df['Season'] == '22-23') & (df['Div'] == 'Bundesliga')]
df_bl.reset_index(inplace=True)
df_bl.drop(df[colunas], axis=1, inplace=True)
df_bl.drop('index', axis=1, inplace=True)

wins_bl = []
draws_bl = []
loses_bl = []

for i in df_bl.index:
    if df_bl.iloc[i]['FTR'] == 'H':
        wins_bl.append(df_bl.iloc[i]['HomeTeam'])
        loses_bl.append(df_bl.iloc[i]['AwayTeam'])
    elif df_bl.iloc[i]['FTR'] == 'A':
        loses_bl.append(df_bl.iloc[i]['HomeTeam'])
        wins_bl.append(df_bl.iloc[i]['AwayTeam'])
    else:
        draws_bl.append(df_bl.iloc[i]['HomeTeam'])
        draws_bl.append(df_bl.iloc[i]['AwayTeam'])

wins_bl = pd.DataFrame(wins_bl, columns=['Team'])
draws_bl = pd.DataFrame(draws_bl, columns=['Team'])
loses_bl = pd.DataFrame(loses_bl, columns=['Team'])

wins_bl = wins_bl['Team'].value_counts().reset_index()
loses_bl = loses_bl['Team'].value_counts().reset_index()
draws_bl = draws_bl['Team'].value_counts().reset_index()

wins_bl.columns = ['Team', 'Count']
loses_bl.columns = ['Team', 'Count']
draws_bl.columns = ['Team', 'Count']

home_score_bl = df_bl.groupby('HomeTeam')['FTHG'].sum().sort_values(ascending=False).reset_index()
home_score_bl.columns = ['Team', 'Goals']
away_score_bl = df_bl.groupby('AwayTeam')['FTAG'].sum().sort_values(ascending=False).reset_index()
away_score_bl.columns = ['Team', 'Goals']
total_score_bl = pd.concat([home_score_bl, away_score_bl])
total_score_bl = total_score_bl.groupby('Team')['Goals'].sum().sort_values(ascending=False).reset_index()

df_bl['HomeWin'] = (df_bl['FTHG'] > df_bl['FTAG']).astype(int)
df_bl['AwayWin'] = (df_bl['FTHG'] < df_bl['FTAG']).astype(int)

df_bl['HomePoints'] = df_bl['HomeWin'] * 3
df_bl['AwayPoints'] = df_bl['AwayWin'] * 3
df_bl['DrawPoints'] = (df_bl['FTHG'] == df_bl['FTAG']).astype(int)

home_points_bl = df_bl.groupby('HomeTeam')['HomePoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'HomePoints': 'Points'})
away_points_bl = df_bl.groupby('AwayTeam')['AwayPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'AwayPoints': 'Points'})

draw_points_home_bl = df_bl.groupby('HomeTeam')['DrawPoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'DrawPoints': 'Points'})
draw_points_away_bl = df_bl.groupby('AwayTeam')['DrawPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'DrawPoints': 'Points'})
total_draw_points_bl = pd.concat([draw_points_home_bl, draw_points_away_bl]).groupby('Team').sum().reset_index()
total_points_bl = pd.concat([home_points_bl, away_points_bl, total_draw_points_bl]).groupby('Team').sum().reset_index()

total_points_bl = total_points_bl.sort_values(by='Points', ascending=False).reset_index()

table_bl = total_points_bl.drop('index', axis=1)

pos_bl = pd.DataFrame()

for date in df_bl['Date'].unique():
    current_matches_bl = df_bl[df_bl['Date'] <= date]
    home_points_bl = current_matches_bl.groupby('HomeTeam')['HomePoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'HomePoints': 'Points'})
    away_points_bl = current_matches_bl.groupby('AwayTeam')['AwayPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'AwayPoints': 'Points'})

    draw_points_home_bl = current_matches_bl.groupby('HomeTeam')['DrawPoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'DrawPoints': 'Points'})
    draw_points_away_bl = current_matches_bl.groupby('AwayTeam')['DrawPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'DrawPoints': 'Points'})
    
    total_draw_points_bl = pd.concat([draw_points_home_bl, draw_points_away_bl]).groupby('Team').sum().reset_index()
    
    total_points_bl = pd.concat([home_points_bl, away_points_bl, total_draw_points_bl]).groupby('Team').sum().reset_index()
    
    total_points_bl['Date'] = date
    total_points_bl['Positions'] = total_points_bl['Points'].rank(method='min', ascending=False)
    
    pos_bl = pd.concat([pos_bl, total_points_bl])


opcoes_bl = list(df_bl.HomeTeam.sort_values().unique())
opcoes_bl.append('Todos')


# Serie A
df_sa = df[(df['Season'] == '22-23') & (df['Div'] == 'Serie A')]
df_sa.reset_index(inplace=True)
df_sa.drop(df[colunas], axis=1, inplace=True)
df_sa.drop('index', axis=1, inplace=True)

wins_sa = []
draws_sa = []
loses_sa = []

for i in df_sa.index:
    if df_sa.iloc[i]['FTR'] == 'H':
        wins_sa.append(df_sa.iloc[i]['HomeTeam'])
        loses_sa.append(df_sa.iloc[i]['AwayTeam'])
    elif df_sa.iloc[i]['FTR'] == 'A':
        loses_sa.append(df_sa.iloc[i]['HomeTeam'])
        wins_sa.append(df_sa.iloc[i]['AwayTeam'])
    else:
        draws_sa.append(df_sa.iloc[i]['HomeTeam'])
        draws_sa.append(df_sa.iloc[i]['AwayTeam'])

wins_sa = pd.DataFrame(wins_sa, columns=['Team'])
draws_sa = pd.DataFrame(draws_sa, columns=['Team'])
loses_sa = pd.DataFrame(loses_sa, columns=['Team'])

wins_sa = wins_sa['Team'].value_counts().reset_index()
loses_sa = loses_sa['Team'].value_counts().reset_index()
draws_sa = draws_sa['Team'].value_counts().reset_index()

wins_sa.columns = ['Team', 'Count']
loses_sa.columns = ['Team', 'Count']
draws_sa.columns = ['Team', 'Count']

home_score_sa = df_sa.groupby('HomeTeam')['FTHG'].sum().sort_values(ascending=False).reset_index()
home_score_sa.columns = ['Team', 'Goals']
away_score_sa = df_sa.groupby('AwayTeam')['FTAG'].sum().sort_values(ascending=False).reset_index()
away_score_sa.columns = ['Team', 'Goals']
total_score_sa = pd.concat([home_score_sa, away_score_sa])
total_score_sa = total_score_sa.groupby('Team')['Goals'].sum().sort_values(ascending=False).reset_index()

df_sa['HomeWin'] = (df_sa['FTHG'] > df_sa['FTAG']).astype(int)
df_sa['AwayWin'] = (df_sa['FTHG'] < df_sa['FTAG']).astype(int)

df_sa['HomePoints'] = df_sa['HomeWin'] * 3
df_sa['AwayPoints'] = df_sa['AwayWin'] * 3
df_sa['DrawPoints'] = (df_sa['FTHG'] == df_sa['FTAG']).astype(int)

home_points_sa = df_sa.groupby('HomeTeam')['HomePoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'HomePoints': 'Points'})
away_points_sa = df_sa.groupby('AwayTeam')['AwayPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'AwayPoints': 'Points'})

draw_points_home_sa = df_sa.groupby('HomeTeam')['DrawPoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'DrawPoints': 'Points'})
draw_points_away_sa = df_sa.groupby('AwayTeam')['DrawPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'DrawPoints': 'Points'})
total_draw_points_sa = pd.concat([draw_points_home_sa, draw_points_away_sa]).groupby('Team').sum().reset_index()
total_points_sa = pd.concat([home_points_sa, away_points_sa, total_draw_points_sa]).groupby('Team').sum().reset_index()

total_points_sa = total_points_sa.sort_values(by='Points', ascending=False).reset_index()

table_sa = total_points_sa.drop('index', axis=1)

pos_sa = pd.DataFrame()

for date in df_sa['Date'].unique():
    current_matches_sa = df_sa[df_sa['Date'] <= date]
    home_points_sa = current_matches_sa.groupby('HomeTeam')['HomePoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'HomePoints': 'Points'})
    away_points_sa = current_matches_sa.groupby('AwayTeam')['AwayPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'AwayPoints': 'Points'})

    draw_points_home_sa = current_matches_sa.groupby('HomeTeam')['DrawPoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'DrawPoints': 'Points'})
    draw_points_away_sa = current_matches_sa.groupby('AwayTeam')['DrawPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'DrawPoints': 'Points'})
    
    total_draw_points_sa = pd.concat([draw_points_home_sa, draw_points_away_sa]).groupby('Team').sum().reset_index()
    
    total_points_sa = pd.concat([home_points_sa, away_points_sa, total_draw_points_sa]).groupby('Team').sum().reset_index()
    
    total_points_sa['Date'] = date
    total_points_sa['Positions'] = total_points_sa['Points'].rank(method='min', ascending=False)
    
    pos_sa = pd.concat([pos_sa, total_points_sa])

opcoes_sa = list(df_sa.HomeTeam.sort_values().unique())
opcoes_sa.append('Todos')


# Ligue 1
df_l1 = df[(df['Season'] == '22-23') & (df['Div'] == 'Ligue 1')]
df_l1.reset_index(inplace=True)
df_l1.drop(df[colunas], axis=1, inplace=True)
df_l1.drop('index', axis=1, inplace=True)

wins_l1 = []
draws_l1 = []
loses_l1 = []

for i in df_l1.index:
    if df_l1.iloc[i]['FTR'] == 'H':
        wins_l1.append(df_l1.iloc[i]['HomeTeam'])
        loses_l1.append(df_l1.iloc[i]['AwayTeam'])
    elif df_l1.iloc[i]['FTR'] == 'A':
        loses_l1.append(df_l1.iloc[i]['HomeTeam'])
        wins_l1.append(df_l1.iloc[i]['AwayTeam'])
    else:
        draws_l1.append(df_l1.iloc[i]['HomeTeam'])
        draws_l1.append(df_l1.iloc[i]['AwayTeam'])

wins_l1 = pd.DataFrame(wins_l1, columns=['Team'])
draws_l1 = pd.DataFrame(draws_l1, columns=['Team'])
loses_l1 = pd.DataFrame(loses_l1, columns=['Team'])

wins_l1 = wins_l1['Team'].value_counts().reset_index()
loses_l1 = loses_l1['Team'].value_counts().reset_index()
draws_l1 = draws_l1['Team'].value_counts().reset_index()

wins_l1.columns = ['Team', 'Count']
loses_l1.columns = ['Team', 'Count']
draws_l1.columns = ['Team', 'Count']

home_score_l1 = df_l1.groupby('HomeTeam')['FTHG'].sum().sort_values(ascending=False).reset_index()
home_score_l1.columns = ['Team', 'Goals']
away_score_l1 = df_l1.groupby('AwayTeam')['FTAG'].sum().sort_values(ascending=False).reset_index()
away_score_l1.columns = ['Team', 'Goals']
total_score_l1 = pd.concat([home_score_l1, away_score_l1])
total_score_l1 = total_score_l1.groupby('Team')['Goals'].sum().sort_values(ascending=False).reset_index()

df_l1['HomeWin'] = (df_l1['FTHG'] > df_l1['FTAG']).astype(int)
df_l1['AwayWin'] = (df_l1['FTHG'] < df_l1['FTAG']).astype(int)

df_l1['HomePoints'] = df_l1['HomeWin'] * 3
df_l1['AwayPoints'] = df_l1['AwayWin'] * 3
df_l1['DrawPoints'] = (df_l1['FTHG'] == df_l1['FTAG']).astype(int)

home_points_l1 = df_l1.groupby('HomeTeam')['HomePoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'HomePoints': 'Points'})
away_points_l1 = df_l1.groupby('AwayTeam')['AwayPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'AwayPoints': 'Points'})

draw_points_home_l1 = df_l1.groupby('HomeTeam')['DrawPoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'DrawPoints': 'Points'})
draw_points_away_l1 = df_l1.groupby('AwayTeam')['DrawPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'DrawPoints': 'Points'})
total_draw_points_l1 = pd.concat([draw_points_home_l1, draw_points_away_l1]).groupby('Team').sum().reset_index()
total_points_l1 = pd.concat([home_points_l1, away_points_l1, total_draw_points_l1]).groupby('Team').sum().reset_index()

total_points_l1 = total_points_l1.sort_values(by='Points', ascending=False).reset_index()

table_l1 = total_points_l1.drop('index', axis=1)

pos_l1 = pd.DataFrame()

for date in df_l1['Date'].unique():
    current_matches_l1 = df_l1[df_l1['Date'] <= date]
    home_points_l1 = current_matches_l1.groupby('HomeTeam')['HomePoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'HomePoints': 'Points'})
    away_points_l1 = current_matches_l1.groupby('AwayTeam')['AwayPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'AwayPoints': 'Points'})

    draw_points_home_l1 = current_matches_l1.groupby('HomeTeam')['DrawPoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'DrawPoints': 'Points'})
    draw_points_away_l1 = current_matches_l1.groupby('AwayTeam')['DrawPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'DrawPoints': 'Points'})
    
    total_draw_points_l1 = pd.concat([draw_points_home_l1, draw_points_away_l1]).groupby('Team').sum().reset_index()
    
    total_points_l1 = pd.concat([home_points_l1, away_points_l1, total_draw_points_l1]).groupby('Team').sum().reset_index()
    
    total_points_l1['Date'] = date
    total_points_l1['Positions'] = total_points_l1['Points'].rank(method='min', ascending=False)
    
    pos_l1 = pd.concat([pos_l1, total_points_l1])

opcoes_l1 = list(df_l1.HomeTeam.sort_values().unique())
opcoes_l1.append('Todos')


def result_graph(df):
    fig = px.bar(df, x = 'Count', y = 'Team')
    fig.update_yaxes(autorange = 'reversed')
    return fig

def score_graph(df):
    fig = px.bar(df, x = 'Goals', y = 'Team')
    fig.update_yaxes(autorange = 'reversed')
    return fig

def table_variance(positions, teams):
    teams = teams
    team_positions = positions[positions['Team'].isin(teams)]

    fig = px.line(team_positions, x = 'Date', y = 'Positions', color='Team', markers=True)

    fig.update_yaxes(autorange = 'reversed', range = [0,18])

    return fig

##################################################################################################
# LAYOUT
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.ModalTitle(children='Análise Top 5 Ligas da Europa 22/23')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='league-dropdown', 
                         value='Premier League(Inglaterra)',
                         options=[
                             {'label': 'Premier League(Inglaterra)', 'value': 'Premier League(Inglaterra)'},
                             {'label': 'LaLiga(Espanha)', 'value': 'LaLiga(Espanha)'},
                             {'label': 'Bundesliga(Alemanha)', 'value': 'Bundesliga(Alemanha)'},
                             {'label': 'Serie A(Italia)', 'value': 'Serie A(Italia)'},
                             {'label': 'Ligue 1(França)', 'value': 'Ligue 1(França)'}
                         ]),
            dcc.Dropdown(id='team-dropdown', value=[], multi=True),
            dcc.Dropdown(
                id='graph-dropdown',
                options=[
                    {'label': 'Tabela', 'value': 'Tabela'},
                    {'label': 'Mais Gols', 'value': 'Mais Gols'},
                    {'label': 'Mais Vitorias', 'value': 'Mais Vitorias'},
                    {'label': 'Mais Empates', 'value': 'Mais Empates'},
                    {'label': 'Mais Derrotas', 'value': 'Mais Derrotas'}
                ],
                value='Tabela'
            ),
            dcc.Graph(id='grafico-mais-gols')
        ])
    ])
])

##################################################################################################
# CALLBACK PARA ATUALIZAR TIMES BASEADO NA LIGA
@app.callback(
    Output('team-dropdown', 'options'),
    [Input('league-dropdown', 'value')]
)
def update_teams(liga):
    if liga == 'Premier League(Inglaterra)':
        return [{'label': team, 'value': team} for team in opcoes_pl]
    elif liga == 'LaLiga(Espanha)':
        return [{'label': team, 'value': team} for team in opcoes_ll]
    elif liga == 'Bundesliga(Alemanha)':
        return [{'label': team, 'value': team} for team in opcoes_bl]
    elif liga == 'Serie A(Italia)':
        return [{'label': team, 'value': team} for team in opcoes_sa]
    elif liga == 'Ligue 1(França)':
        return [{'label': team, 'value': team} for team in opcoes_l1]

##################################################################################################
# CALLBACK PARA ATUALIZAR GRÁFICO
@app.callback(
    Output('grafico-mais-gols', 'figure'),
    [Input('league-dropdown', 'value'),
     Input('team-dropdown', 'value'),
     Input('graph-dropdown', 'value')]
)
def update_graph(liga, equipe, grafico):
    if liga == 'Premier League(Inglaterra)':
        total_score_filtered = total_score_pl[total_score_pl['Team'].isin(equipe)] if 'Todos' not in equipe else total_score_pl
        wins_filtered = wins_pl[wins_pl['Team'].isin(equipe)] if 'Todos' not in equipe else wins_pl
        draws_filtered = draws_pl[draws_pl['Team'].isin(equipe)] if 'Todos' not in equipe else draws_pl
        loses_filtered = loses_pl[loses_pl['Team'].isin(equipe)] if 'Todos' not in equipe else loses_pl
        positions_filtered = pos_pl[pos_pl['Team'].isin(equipe)] if 'Todos' not in equipe else pos_pl
    
    elif liga == 'LaLiga(Espanha)':
        total_score_filtered = total_score_ll[total_score_ll['Team'].isin(equipe)] if 'Todos' not in equipe else total_score_ll
        wins_filtered = wins_ll[wins_ll['Team'].isin(equipe)] if 'Todos' not in equipe else wins_ll
        draws_filtered = draws_ll[draws_ll['Team'].isin(equipe)] if 'Todos' not in equipe else draws_ll
        loses_filtered = loses_ll[loses_ll['Team'].isin(equipe)] if 'Todos' not in equipe else loses_ll
        positions_filtered = pos_ll[pos_ll['Team'].isin(equipe)] if 'Todos' not in equipe else pos_ll

    elif liga == 'Bundesliga(Alemanha)':
        total_score_filtered = total_score_bl[total_score_bl['Team'].isin(equipe)] if 'Todos' not in equipe else total_score_bl
        wins_filtered = wins_bl[wins_bl['Team'].isin(equipe)] if 'Todos' not in equipe else wins_bl
        draws_filtered = draws_bl[draws_bl['Team'].isin(equipe)] if 'Todos' not in equipe else draws_bl
        loses_filtered = loses_bl[loses_bl['Team'].isin(equipe)] if 'Todos' not in equipe else loses_bl
        positions_filtered = pos_bl[pos_bl['Team'].isin(equipe)] if 'Todos' not in equipe else pos_bl

    elif liga == 'Serie A(Italia)':
        total_score_filtered = total_score_sa[total_score_sa['Team'].isin(equipe)] if 'Todos' not in equipe else total_score_sa
        wins_filtered = wins_sa[wins_sa['Team'].isin(equipe)] if 'Todos' not in equipe else wins_sa
        draws_filtered = draws_sa[draws_sa['Team'].isin(equipe)] if 'Todos' not in equipe else draws_sa
        loses_filtered = loses_sa[loses_sa['Team'].isin(equipe)] if 'Todos' not in equipe else loses_sa
        positions_filtered = pos_sa[pos_sa['Team'].isin(equipe)] if 'Todos' not in equipe else pos_sa

    elif liga == 'Ligue 1(França)':
        total_score_filtered = total_score_l1[total_score_l1['Team'].isin(equipe)] if 'Todos' not in equipe else total_score_l1
        wins_filtered = wins_l1[wins_l1['Team'].isin(equipe)] if 'Todos' not in equipe else wins_l1
        draws_filtered = draws_l1[draws_l1['Team'].isin(equipe)] if 'Todos' not in equipe else draws_l1
        loses_filtered = loses_l1[loses_l1['Team'].isin(equipe)] if 'Todos' not in equipe else loses_l1
        positions_filtered = pos_l1[pos_l1['Team'].isin(equipe)] if 'Todos' not in equipe else pos_l1


    if grafico == 'Mais Gols':
        return score_graph(total_score_filtered)
    elif grafico == 'Mais Vitorias':
        return result_graph(wins_filtered)
    elif grafico == 'Mais Empates':
        return result_graph(draws_filtered)
    elif grafico == 'Mais Derrotas':
        return result_graph(loses_filtered)
    elif grafico == 'Tabela':
        return table_variance(positions_filtered, equipe)

if __name__ == '__main__':
    app.run_server(debug=True)