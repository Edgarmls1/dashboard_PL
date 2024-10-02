from dash import Dash, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


app = Dash(__name__)


df = pd.read_csv('past-data.csv')

df = df[(df['Season'] == '22-23') & (df['Div'] == 'Premier League')]

colunas = ['Season', 'Div', 'Time', 'HTHG', 'HTAG', 'HTR', 'Referee', 'HC', 'AC', 'HF', 'AF', 'HY', 'AY', 'HR', 'AR', 'HS', 'AS', 'HST', 'AST']
# justificativa da retirada de colunas
# season, div -> todos os valores sao os mesmos
# time, HTHG, HTAG, HTR, HC, AC, HF, AF, HY, AY, HR, AR, HS, AS, HST, AST, referee -> nao serao analisados

df.drop(df[colunas], axis=1, inplace=True)

# total de gols marcados
home_score = df.groupby('HomeTeam')['FTHG'].sum().sort_values(ascending=False).reset_index()
home_score.columns = ['Team', 'Goals']
away_score = df.groupby('AwayTeam')['FTAG'].sum().sort_values(ascending=False).reset_index()
away_score.columns = ['Team', 'Goals']
total_score = pd.concat([home_score, away_score])
total_score = total_score.groupby('Team')['Goals'].sum().sort_values(ascending=False).reset_index()

home_conceded = df.groupby('HomeTeam')['FTAG'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'FTAG': 'HomeConceded'})
away_conceded = df.groupby('AwayTeam')['FTHG'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'FTHG': 'AwayConceded'})

home_score['HomeGoalDifference'] = home_score['Goals'] - home_conceded['HomeConceded']
away_score['AwayGoalDifference'] = away_score['Goals'] - away_conceded['AwayConceded']

goal_difference = pd.merge(home_score[['Team', 'HomeGoalDifference']], away_score[['Team', 'AwayGoalDifference']], on='Team')

goal_difference['TotalGoalDifference'] = goal_difference['HomeGoalDifference'] + goal_difference['AwayGoalDifference']

goal_difference = goal_difference.sort_values(by='TotalGoalDifference', ascending=False).reset_index(drop=True)
#

# Tabela de pontuação
df['HomeWin'] = (df['FTHG'] > df['FTAG']).astype(int)
df['AwayWin'] = (df['FTHG'] < df['FTAG']).astype(int)

df['HomePoints'] = df['HomeWin'] * 3
df['AwayPoints'] = df['AwayWin'] * 3
df['DrawPoints'] = (df['FTHG'] == df['FTAG']).astype(int)

home_points = df.groupby('HomeTeam')['HomePoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'HomePoints': 'Points'})
away_points = df.groupby('AwayTeam')['AwayPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'AwayPoints': 'Points'})

draw_points_home = df.groupby('HomeTeam')['DrawPoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'DrawPoints': 'Points'})
draw_points_away = df.groupby('AwayTeam')['DrawPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'DrawPoints': 'Points'})
total_draw_points = pd.concat([draw_points_home, draw_points_away]).groupby('Team').sum().reset_index()
total_points = pd.concat([home_points, away_points, total_draw_points]).groupby('Team').sum().reset_index()

total_points = total_points.sort_values(by='Points', ascending=False).reset_index()
table = total_points.drop('index', axis=1)
table['Points Mean'] = table['Points']/38
table = table.merge(goal_difference, on= 'Team')
table = table.drop(['HomeGoalDifference','AwayGoalDifference'], axis=1)

positions = pd.DataFrame()

for date in df['Date'].unique():
    current_matches = df[df['Date'] <= date]
    home_points = current_matches.groupby('HomeTeam')['HomePoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'HomePoints': 'Points'})
    away_points = current_matches.groupby('AwayTeam')['AwayPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'AwayPoints': 'Points'})
    total_points = pd.concat([home_points, away_points]).groupby('Team').sum().reset_index()

    total_points['Date'] = date
    total_points['Positions'] = total_points['Points'].rank(method='min', ascending=False)

    positions = pd.concat([positions, total_points])
#

# Calculando vitorias, empates e derrotas
wins = []
draws = []
loses = []

for i in df.index:
    if df.iloc[i]['FTR'] == 'H':
        wins.append(df.iloc[i]['HomeTeam'])
        loses.append(df.iloc[i]['AwayTeam'])
    elif df.iloc[i]['FTR'] == 'A':
        loses.append(df.iloc[i]['HomeTeam'])
        wins.append(df.iloc[i]['AwayTeam'])
    else:
        draws.append(df.iloc[i]['HomeTeam'])
        draws.append(df.iloc[i]['AwayTeam'])

wins = pd.DataFrame(wins, columns=['Team'])
draws = pd.DataFrame(draws, columns=['Team'])
loses = pd.DataFrame(loses, columns=['Team'])

wins = wins['Team'].value_counts().reset_index()
loses = loses['Team'].value_counts().reset_index()
draws = draws['Team'].value_counts().reset_index()

wins.columns = ['Team', 'Count']
loses.columns = ['Team', 'Count']
draws.columns = ['Team', 'Count']
#

opcoes = list(df.HomeTeam.sort_values().unique())

opcoes.append('Todos')

##################################################################################################
# LAYOUT
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.ModalTitle(children='Analise Premier League 22/23')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='graph-dropdown',
                options=['Tabela', 'Mais Gols', 'Mais Vitorias', 'Mais Empates', 'Mais Derrotas'],
                value='Tabela'
            ),
            dcc.Dropdown(opcoes, value=['Man City'], id='team-dropdown', multi=True),
            dcc.Graph(id='grafico')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.ModalTitle(children='Tabela da temporada 22/23'),

            dash_table.DataTable(
                id='data-table',
                data=table.to_dict('records'),
                style_table={
                    'width': '20%',
                    'height': 'auto'
                },
                style_cell={
                    'textAlign': 'left',
                    'minWidth': '50px',
                    'width': '80px',
                    'maxWidth': '80px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'fontSize': '12px',
                },
                style_data_conditional=[
                    {
                        'if': {'filter_query': '{Points} <= 35'},
                        'backgroundColor': '#FF4136',
                    },
                    {
                        'if': {'filter_query': '{Points} > 70'},
                        'backgroundColor': '#3D9970',
                        'color': 'white'
                    },
                    {
                        'if': {'column_id': 'Team'},
                        'backgroundColor': '#FFFFFF',
                        'color': 'black'
                    },
                    {
                        'if': {'column_id': 'TotalGoalDifference'},
                        'backgroundColor': '#FFFFFF',
                        'color': 'black'
                    },
                    {
                        'if': {'column_id': 'Points Mean'},
                        'backgroundColor': '#FFFFFF',
                        'color': 'black'
                    }
                ]
            )
        ])
    ])
])

##################################################################################################
# CALLBACK
@app.callback(
    Output('grafico', 'figure'),
    [Input('team-dropdown', 'value'),
     Input('graph-dropdown', 'value')]
)
def update_graph(equipe, grafico):

    if 'Todos' not in equipe:
        total_score_filtered = total_score[total_score['Team'].isin(equipe)]
        wins_filtered = wins[wins['Team'].isin(equipe)]
        draws_filtered = draws[draws['Team'].isin(equipe)]
        loses_filtered = loses[loses['Team'].isin(equipe)]
        positions_filtered = positions[positions['Team'].isin(equipe)]
    else:
        total_score_filtered = total_score
        wins_filtered = wins
        draws_filtered = draws
        loses_filtered = loses
        positions_filtered = positions

    if grafico == 'Mais Gols':
        fig = px.bar(total_score_filtered, x='Goals', y='Team', title='Times com mais gols')
        fig.update_yaxes(autorange='reversed')

    elif grafico == 'Mais Vitorias':
        fig = px.bar(wins_filtered, x='Count', y='Team', title='Times com mais vitórias')
        fig.update_yaxes(autorange='reversed')

    elif grafico == 'Mais Empates':
        fig = px.bar(draws_filtered, x='Count', y='Team', title='Times com mais empates')
        fig.update_yaxes(autorange='reversed')

    elif grafico == 'Mais Derrotas':
        fig = px.bar(loses_filtered, x='Count', y='Team', title='Times com mais derrotas')
        fig.update_yaxes(autorange='reversed')

    elif grafico == 'Tabela':
        fig = px.line(positions_filtered, x='Date', y='Positions', color='Team', markers=True)
        fig.update_yaxes(autorange='reversed', range=[0, 18])

    return fig


if __name__ == '__main__':
    app.run_server(debug = True)
