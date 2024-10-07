# Dashboard de Análise das Top 5 Ligas Europeias na Temporada 22/23

Este Dashboard foi criado utilizando a linguagem Python, com auxílio da biblioteca **Dash** para visualização e análise de dados da temporada 2022/2023 das 5 principais ligas do futebol europeu: **Premier League**, **LaLiga**, **Bundesliga**, **Serie A** e **Ligue 1**. Os dados foram coletados da plataforma **Kaggle** e permitem uma análise interativa sobre o desempenho dos times em diversas métricas, como gols marcados, vitórias, empates, derrotas e a variação de posição ao longo da temporada.

## Funcionalidades

O Dashboard oferece as seguintes opções de análise:
- **Tabela de Pontuação**: Exibe a classificação final dos times na temporada com o total de pontos e a diferença de gols.
- **Times com Mais Gols**: Mostra quais times marcaram mais gols ao longo da temporada.
- **Times com Mais Vitórias**: Lista os times que mais venceram.
- **Times com Mais Empates**: Apresenta os times com o maior número de empates.
- **Times com Mais Derrotas**: Informa os times que mais perderam.
- **Variação de Posição**: Permite visualizar como as posições dos times mudaram ao longo do campeonato, de acordo com as datas dos jogos.

## Estrutura do Código

### Importação de Bibliotecas
As seguintes bibliotecas são utilizadas no projeto:
- **Dash**: Para a construção do layout interativo.
- **Dash Bootstrap Components (dbc)**: Para estilização e layout utilizando componentes prontos do Bootstrap.
- **Plotly Express (px)**: Para gerar gráficos dinâmicos e interativos.
- **Pandas**: Para manipulação e processamento dos dados da temporada.
- **Dash DataTable**: Para exibição da tabela de pontuação.

### Carregamento e Processamento de Dados
Os dados são carregados a partir de um arquivo CSV contendo informações detalhadas sobre os jogos da temporada. O código realiza as seguintes operações:
- Filtra a temporada 22/23 e a divisão correspondente.
- Cria colunas que calculam a pontuação e a diferença de gols dos times.
- Agrupa os dados para determinar o número total de gols marcados, gols sofridos e a diferença de gols.

### Cálculo de Pontuação
O código implementa a seguinte lógica para calcular a pontuação dos times:
- **Vitória em casa**: 3 pontos.
- **Vitória fora de casa**: 3 pontos.
- **Empate**: 1 ponto para cada time.

### Layout do Dashboard
O layout do Dashboard é definido utilizando componentes do **Dash** e **Bootstrap** para criar uma interface amigável. O usuário pode selecionar:
1. **Liga/País**: Dropdown que permite o usuário escolher qual liga será analisada.
2. **Tipo de gráfico**: Usando um dropdown, o usuário escolhe entre as opções de análise disponíveis (gols, vitórias, empates, derrotas ou tabela).
3. **Times**: Outro dropdown permite selecionar um ou mais times para visualização personalizada.

### Gráficos e Tabela
Dependendo da seleção feita nos dropdowns, o código atualiza o gráfico exibido, podendo mostrar:
- Um gráfico de barras com os times e seus respectivos valores (gols, vitórias, empates ou derrotas).
- Um gráfico de linhas mostrando a variação da posição dos times ao longo da temporada.

Além disso, a tabela exibe o total de pontos e a diferença de gols de cada time, com estilização condicional para destacar os times com pontuações mais baixas ou mais altas.

## Observações Finais

Este Dashboard oferece uma maneira intuitiva e visual de analisar os dados das top 5 ligas europeias, fornecendo insights rápidos sobre o desempenho dos times. É uma ferramenta valiosa para quem deseja entender a performance dos times durante a temporada 22/23.
