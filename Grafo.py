# ================================
# Instalação das Bibliotecas Necessárias
# ================================
# !pip install networkx matplotlib pandas seaborn
# !pip install python-louvain

# ================================
# Importação das Bibliotecas
# ================================
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.patches as mpatches
import statistics

# Ajuste para a biblioteca de modularidade (python-louvain)
try:
    import community.community_louvain as community_louvain
    modularidade_disponivel = True
except ImportError:
    modularidade_disponivel = False

# ================================
# Passo 1: Organização dos Dados das Estações
# ================================
estacoes_data = [
    # Linha 1 - Azul
    {"nome": "Jabaquara", "linha": "Linha 1 - Azul", "ordem": 1},
    {"nome": "Conceição", "linha": "Linha 1 - Azul", "ordem": 2},
    {"nome": "São Judas", "linha": "Linha 1 - Azul", "ordem": 3},
    {"nome": "Saúde", "linha": "Linha 1 - Azul", "ordem": 4},
    {"nome": "Praça da Árvore", "linha": "Linha 1 - Azul", "ordem": 5},
    {"nome": "Santa Cruz", "linha": "Linha 1 - Azul", "ordem": 6},
    {"nome": "Vila Mariana", "linha": "Linha 1 - Azul", "ordem": 7},
    {"nome": "Ana Rosa", "linha": "Linha 1 - Azul", "ordem": 8},
    {"nome": "Paraíso", "linha": "Linha 1 - Azul", "ordem": 9},
    {"nome": "Vergueiro", "linha": "Linha 1 - Azul", "ordem": 10},
    {"nome": "São Joaquim", "linha": "Linha 1 - Azul", "ordem": 11},
    {"nome": "Japão-Liberdade", "linha": "Linha 1 - Azul", "ordem": 12},
    {"nome": "Sé", "linha": "Linha 1 - Azul", "ordem": 13},
    {"nome": "São Bento", "linha": "Linha 1 - Azul", "ordem": 14},
    {"nome": "Luz", "linha": "Linha 1 - Azul", "ordem": 15},
    {"nome": "Tiradentes", "linha": "Linha 1 - Azul", "ordem": 16},
    {"nome": "Armênia", "linha": "Linha 1 - Azul", "ordem": 17},
    {"nome": "Portuguesa-Tietê", "linha": "Linha 1 - Azul", "ordem": 18},
    {"nome": "Carandiru", "linha": "Linha 1 - Azul", "ordem": 19},
    {"nome": "Santana", "linha": "Linha 1 - Azul", "ordem": 20},
    {"nome": "Jardim São Paulo-Ayrton Senna", "linha": "Linha 1 - Azul", "ordem": 21},
    {"nome": "Parada Inglesa", "linha": "Linha 1 - Azul", "ordem": 22},
    {"nome": "Tucuruvi", "linha": "Linha 1 - Azul", "ordem": 23},

    # Linha 2 - Verde
    {"nome": "Vila Prudente", "linha": "Linha 2 - Verde", "ordem": 1},
    {"nome": "Tamanduateí", "linha": "Linha 2 - Verde", "ordem": 2},
    {"nome": "Sacomã", "linha": "Linha 2 - Verde", "ordem": 3},
    {"nome": "Alto do Ipiranga", "linha": "Linha 2 - Verde", "ordem": 4},
    {"nome": "Santos-Imigrantes", "linha": "Linha 2 - Verde", "ordem": 5},
    {"nome": "Chácara Klabin", "linha": "Linha 2 - Verde", "ordem": 6},
    {"nome": "Ana Rosa", "linha": "Linha 2 - Verde", "ordem": 7},
    {"nome": "Paraíso", "linha": "Linha 2 - Verde", "ordem": 8},
    {"nome": "Brigadeiro", "linha": "Linha 2 - Verde", "ordem": 9},
    {"nome": "Trianon-Masp", "linha": "Linha 2 - Verde", "ordem": 10},
    {"nome": "Consolação", "linha": "Linha 2 - Verde", "ordem": 11},
    {"nome": "Clínicas", "linha": "Linha 2 - Verde", "ordem": 12},
    {"nome": "S. N. Sra. de Fátima-Sumaré", "linha": "Linha 2 - Verde", "ordem": 13},
    {"nome": "Vila Madalena", "linha": "Linha 2 - Verde", "ordem": 14},

    # Linha 3 - Vermelha
    {"nome": "Corinthians-Itaquera", "linha": "Linha 3 - Vermelha", "ordem": 1},
    {"nome": "Artur Alvim", "linha": "Linha 3 - Vermelha", "ordem": 2},
    {"nome": "Patriarca-Vila Ré", "linha": "Linha 3 - Vermelha", "ordem": 3},
    {"nome": "Guilhermina-Esperança", "linha": "Linha 3 - Vermelha", "ordem": 4},
    {"nome": "Vila Matilde", "linha": "Linha 3 - Vermelha", "ordem": 5},
    {"nome": "Penha", "linha": "Linha 3 - Vermelha", "ordem": 6},
    {"nome": "Carrão-Assaí Atacadista", "linha": "Linha 3 - Vermelha", "ordem": 7},
    {"nome": "Tatuapé", "linha": "Linha 3 - Vermelha", "ordem": 8},
    {"nome": "Belém", "linha": "Linha 3 - Vermelha", "ordem": 9},
    {"nome": "Bresser-Mooca", "linha": "Linha 3 - Vermelha", "ordem": 10},
    {"nome": "Brás", "linha": "Linha 3 - Vermelha", "ordem": 11},
    {"nome": "Pedro II", "linha": "Linha 3 - Vermelha", "ordem": 12},
    {"nome": "Sé", "linha": "Linha 3 - Vermelha", "ordem": 13},
    {"nome": "Anhangabaú", "linha": "Linha 3 - Vermelha", "ordem": 14},
    {"nome": "República", "linha": "Linha 3 - Vermelha", "ordem": 15},
    {"nome": "Santa Cecília", "linha": "Linha 3 - Vermelha", "ordem": 16},
    {"nome": "Marechal Deodoro", "linha": "Linha 3 - Vermelha", "ordem": 17},
    {"nome": "Palmeiras-Barra Funda", "linha": "Linha 3 - Vermelha", "ordem": 18},

    # Linha 4 - Amarela
    {"nome": "Luz", "linha": "Linha 4 - Amarela", "ordem": 1},
    {"nome": "República", "linha": "Linha 4 - Amarela", "ordem": 2},
    {"nome": "Higienópolis-Mackenzie", "linha": "Linha 4 - Amarela", "ordem": 3},
    {"nome": "Paulista", "linha": "Linha 4 - Amarela", "ordem": 4},
    {"nome": "Oscar Freire", "linha": "Linha 4 - Amarela", "ordem": 5},
    {"nome": "Fradique Coutinho", "linha": "Linha 4 - Amarela", "ordem": 6},
    {"nome": "Faria Lima", "linha": "Linha 4 - Amarela", "ordem": 7},
    {"nome": "Pinheiros", "linha": "Linha 4 - Amarela", "ordem": 8},
    {"nome": "Butantã", "linha": "Linha 4 - Amarela", "ordem": 9},
    {"nome": "São Paulo-Morumbi", "linha": "Linha 4 - Amarela", "ordem": 10},
    {"nome": "Vila Sônia", "linha": "Linha 4 - Amarela", "ordem": 11},

    # Linha 5 - Lilás
    {"nome": "Capão Redondo", "linha": "Linha 5 - Lilás", "ordem": 1},
    {"nome": "Campo Limpo", "linha": "Linha 5 - Lilás", "ordem": 2},
    {"nome": "Vila das Belezas", "linha": "Linha 5 - Lilás", "ordem": 3},
    {"nome": "Giovanni Gronchi", "linha": "Linha 5 - Lilás", "ordem": 4},
    {"nome": "Santo Amaro", "linha": "Linha 5 - Lilás", "ordem": 5},
    {"nome": "Largo Treze", "linha": "Linha 5 - Lilás", "ordem": 6},
    {"nome": "Adolfo Pinheiro", "linha": "Linha 5 - Lilás", "ordem": 7},
    {"nome": "Alto da Boa Vista", "linha": "Linha 5 - Lilás", "ordem": 8},
    {"nome": "Borba Gato", "linha": "Linha 5 - Lilás", "ordem": 9},
    {"nome": "Brooklin", "linha": "Linha 5 - Lilás", "ordem": 10},
    {"nome": "Campo Belo", "linha": "Linha 5 - Lilás", "ordem": 11},
    {"nome": "Eucaliptos", "linha": "Linha 5 - Lilás", "ordem": 12},
    {"nome": "Moema", "linha": "Linha 5 - Lilás", "ordem": 13},
    {"nome": "AACD-Servidor", "linha": "Linha 5 - Lilás", "ordem": 14},
    {"nome": "Hospital São Paulo", "linha": "Linha 5 - Lilás", "ordem": 15},
    {"nome": "Santa Cruz", "linha": "Linha 5 - Lilás", "ordem": 16},
    {"nome": "Chácara Klabin", "linha": "Linha 5 - Lilás", "ordem": 17},

    # Linha 15 - Prata
    {"nome": "Vila Prudente", "linha": "Linha 15 - Prata", "ordem": 1},
    {"nome": "Oratório", "linha": "Linha 15 - Prata", "ordem": 2},
    {"nome": "São Lucas", "linha": "Linha 15 - Prata", "ordem": 3},
    {"nome": "Camilo Haddad", "linha": "Linha 15 - Prata", "ordem": 4},
    {"nome": "Vila Tolstói", "linha": "Linha 15 - Prata", "ordem": 5},
    {"nome": "Vila União", "linha": "Linha 15 - Prata", "ordem": 6},
    {"nome": "Jardim Planalto", "linha": "Linha 15 - Prata", "ordem": 7},
    {"nome": "Sapopemba", "linha": "Linha 15 - Prata", "ordem": 8},
    {"nome": "Fazenda da Juta", "linha": "Linha 15 - Prata", "ordem": 9},
    {"nome": "São Mateus", "linha": "Linha 15 - Prata", "ordem": 10},
    {"nome": "Jardim Colonial", "linha": "Linha 15 - Prata", "ordem": 11},
]

# Criação do DataFrame
estacoes_df = pd.DataFrame(estacoes_data)

# Verificar estações que pertencem a múltiplas linhas (Estação com Baldiação)
duplicatas = estacoes_df[estacoes_df.duplicated(subset=['nome'], keep=False)].sort_values('nome')
print("Estações que pertencem a múltiplas linhas:")
print(duplicatas[['nome', 'linha']].sort_values('nome').to_string(index=False))

# ================================
# Passo 2: Construção do Grafo
# ================================
G = nx.Graph()

# Adicionar nós
for idx, row in estacoes_df.iterrows():
    nome = row['nome']
    linha = row['linha']

    if G.has_node(nome):
        if linha not in G.nodes[nome]['linha']:
            G.nodes[nome]['linha'].append(linha)
    else:
        G.add_node(nome, linha=[linha])

# Adicionar arestas
linhas = estacoes_df.groupby('linha')
for linha, group in linhas:
    estacoes = group.sort_values('ordem')['nome'].tolist()
    for i in range(len(estacoes) - 1):
        origem = estacoes[i]
        destino = estacoes[i + 1]
        if G.has_edge(origem, destino):
            if linha not in G[origem][destino]['linha']:
                G[origem][destino]['linha'].append(linha)
        else:
            G.add_edge(origem, destino, linha=[linha])

print(f"\nGrafo criado com {G.number_of_nodes()} nós e {G.number_of_edges()} arestas.")

# ================================
# Passo 3: Atribuição de Pesos às Arestas
# ================================
graus = dict(G.degree())
for u, v, data in G.edges(data=True):
    peso = graus[u] + graus[v]
    G[u][v]['peso'] = peso

print("\nExemplos de pesos das arestas:")
for i, (u, v, data) in enumerate(G.edges(data=True)):
    if i < 5:
        print(f"{u} - {v}: Peso = {data['peso']}")

# ================================
# Passo 4: Cálculo de Métricas de Centralidade
# ================================
grau = nx.degree_centrality(G)
grau_df = pd.DataFrame.from_dict(grau, orient='index', columns=['Grau_Centralidade'])

betweenness = nx.betweenness_centrality(G, weight='peso')
betweenness_df = pd.DataFrame.from_dict(betweenness, orient='index', columns=['Betweenness_Centralidade'])

closeness = nx.closeness_centrality(G)
closeness_df = pd.DataFrame.from_dict(closeness, orient='index', columns=['Closeness_Centralidade'])

metrics_df = grau_df.join(betweenness_df).join(closeness_df)
metrics_df = metrics_df.sort_values(by='Betweenness_Centralidade', ascending=False)

print("\nTop 10 Estações por Centralidade de Betweenness:")
print(metrics_df['Betweenness_Centralidade'].head(10))

# ================================
# Passo 5: Visualização do Grafo
# ================================
linha_cores = {
    "Linha 1 - Azul": "#0041C2",
    "Linha 2 - Verde": "#00923F",
    "Linha 3 - Vermelha": "#FF0000",
    "Linha 4 - Amarela": "#FFD700",
    "Linha 5 - Lilás": "#A020F0",
    "Linha 15 - Prata": "#C0C0C0"
}

def get_edge_color(linhas):
    return linha_cores.get(linhas[0], "gray")

def is_transfer_station(linhas):
    return len(linhas) > 1

for node in G.nodes():
    G.nodes[node]['transfer'] = is_transfer_station(G.nodes[node]['linha'])

pos = nx.spring_layout(G, k=0.3, seed=42)

plt.figure(figsize=(25, 25))
plt.title("Grafo do Metrô de São Paulo", fontsize=25)

for edge in G.edges(data=True):
    linhas = edge[2]['linha']
    color = get_edge_color(linhas)
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[(edge[0], edge[1])],
        edge_color=color,
        width=2,
        alpha=0.7
    )

num_linhas = {node: len(data['linha']) for node, data in G.nodes(data=True)}
node_sizes = [800 * num_linhas[node] for node in G.nodes()]
node_colors = ['red' if G.nodes[node]['transfer'] else 'white' for node in G.nodes()]

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=node_sizes,
    node_color=node_colors,
    edgecolors='black',
    linewidths=1.5,
    alpha=0.9
)

labels = {}
for node, data in G.nodes(data=True):
    if data['transfer']:
        labels[node] = f"{node}\n(Estação com Baldiação)"
    else:
        labels[node] = node

nx.draw_networkx_labels(
    G,
    pos,
    labels,
    font_size=8,
    font_color='black'
)

legenda_linhas = [mpatches.Patch(color=cor, label=linha) for linha, cor in linha_cores.items()]
legenda_transfer = mpatches.Patch(color='red', label='Estação com Baldiação')
legendas = legenda_linhas + [legenda_transfer]

plt.legend(handles=legendas, loc='upper right', fontsize='large', title='Linhas do Metrô e Transferências')
plt.axis('off')
plt.tight_layout()
plt.show()

# ================================
# Passo 6: Criação de Gráficos das Métricas de Centralidade
# ================================
sns.set(style="whitegrid")

# Função para criar gráfico de barras de uma métrica
def plot_metric_top10(series, title, ylabel, palette="viridis"):
    top10 = series.nlargest(10)
    plt.figure(figsize=(16, 8))
    sns.barplot(x=top10.index, y=top10.values, palette=palette)
    plt.title(title, fontsize=18)
    plt.xlabel("Estações", fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()

plot_metric_top10(metrics_df['Betweenness_Centralidade'], "Top 10 Estações por Centralidade de Betweenness", "Centralidade de Betweenness", "viridis")
plot_metric_top10(metrics_df['Closeness_Centralidade'], "Top 10 Estações por Centralidade de Closeness", "Centralidade de Closeness", "magma")
plot_metric_top10(metrics_df['Grau_Centralidade'], "Top 10 Estações por Grau de Centralidade", "Grau de Centralidade", "coolwarm")

# ================================
# Passo 7: Análises Adicionais
# ================================
origem = "Jabaquara"
destino = "São Mateus"

try:
    rota = nx.shortest_path(G, source=origem, target=destino, weight='peso')
    peso_total = sum([G.edges[rota[i], rota[i+1]]['peso'] for i in range(len(rota)-1)])
    print(f"\nRota mais curta de {origem} para {destino}:")
    print(" -> ".join(rota))
    print(f"Peso total estimado: {peso_total}")
except nx.NetworkXNoPath:
    print(f"Não há caminho entre {origem} e {destino}.")

max_betweenness = betweenness_df['Betweenness_Centralidade'].idxmax()
print(f"\nEstação com maior centralidade de betweenness: {max_betweenness}")
print(f"Valor: {betweenness_df.loc[max_betweenness, 'Betweenness_Centralidade']}")

min_grau = grau_df['Grau_Centralidade'].nsmallest(5)
print("\n5 Estações com menor grau de centralidade:")
print(min_grau)

estacao_remover = max_betweenness
G_resiliente = G.copy()
G_resiliente.remove_node(estacao_remover)

num_componentes_original = nx.number_connected_components(G)
num_componentes_resiliente = nx.number_connected_components(G_resiliente)
print(f"\nNúmero de Componentes Conectados antes da remoção: {num_componentes_original}")
print(f"Número de Componentes Conectados após a remoção de {estacao_remover}: {num_componentes_resiliente}")

estacoes_baixa_centralidade = metrics_df.sort_values('Betweenness_Centralidade').head(5).index.tolist()
print("\nEstações com baixa centralidade de betweenness (sugestões para expansão):")
for estacao in estacoes_baixa_centralidade:
    print(f"- {estacao}")

# ================================
# Métricas adicionais
# ================================
grau_medio = sum(dict(G.degree()).values()) / G.number_of_nodes()

# Diâmetro, Raio (considerando componente maior se não for conectado)
if nx.is_connected(G):
    diametro = nx.diameter(G)
    raio = nx.radius(G)
    avg_shortest_path_length = nx.average_shortest_path_length(G, weight='peso')
else:
    componentes = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    maior_componente = max(componentes, key=lambda c: c.number_of_nodes())
    diametro = nx.diameter(maior_componente)
    raio = nx.radius(maior_componente)
    avg_shortest_path_length = nx.average_shortest_path_length(maior_componente, weight='peso')

densidade = nx.density(G)

if modularidade_disponivel:
    partition = community_louvain.best_partition(G)
    modularidade = community_louvain.modularity(partition, G)
else:
    modularidade = None

pagerank = nx.pagerank(G, alpha=0.85)
pagerank_df = pd.DataFrame.from_dict(pagerank, orient='index', columns=['PageRank'])

num_componentes = nx.number_connected_components(G)
coeficiente_clusterizacao = nx.average_clustering(G)

# Métricas adicionais:
transitividade = nx.transitivity(G)
componentes = [G.subgraph(c).copy() for c in nx.connected_components(G)]
maior_componente = max(componentes, key=lambda c: c.number_of_nodes())
ecc = nx.eccentricity(maior_componente)
eccentricidade_media = statistics.mean(ecc.values())
degree_assortativity = nx.degree_assortativity_coefficient(G)

print("\n===== Métricas Adicionais =====")
print(f"Grau Médio: {grau_medio}")
print(f"Diametro: {diametro}")
print(f"Raio: {raio}")
print(f"Densidade do Grafo: {densidade}")
print(f"Transitividade: {transitividade}")
print(f"Eccentricidade Média (Maior Componente): {eccentricidade_media}")
print(f"Degree Assortativity: {degree_assortativity}")
print(f"Comprimento Médio dos Caminhos (Maior Componente): {avg_shortest_path_length}")
if modularidade is not None:
    print(f"Modularidade: {modularidade}")
else:
    print("Modularidade: Não foi possível calcular (biblioteca python-louvain não instalada ou erro na importação).")
print(f"Número de Componentes Conectados: {num_componentes}")
print(f"Coeficiente de Clusterização Médio: {coeficiente_clusterizacao}")

print("\nTop 10 Estações por PageRank:")
print(pagerank_df['PageRank'].nlargest(10))

# Gráfico dos Top 10 Estações por PageRank
plot_metric_top10(pagerank_df['PageRank'], "Top 10 Estações por PageRank", "PageRank", "plasma")

# ================================
# Criação de Gráficos de Distribuição
# ================================
degree_values = [G.degree(n) for n in G.nodes()]
plt.figure(figsize=(10, 6))
sns.histplot(degree_values, kde=True, color='blue')
plt.title("Distribuição de Grau das Estações", fontsize=16)
plt.xlabel("Grau", fontsize=14)
plt.ylabel("Frequência", fontsize=14)
plt.tight_layout()
plt.show()

# Distribuição da Centralidade de Betweenness
plt.figure(figsize=(10, 6))
sns.histplot(metrics_df['Betweenness_Centralidade'], kde=True, color='green')
plt.title("Distribuição da Centralidade de Betweenness", fontsize=16)
plt.xlabel("Betweenness", fontsize=14)
plt.ylabel("Frequência", fontsize=14)
plt.tight_layout()
plt.show()

# Distribuição da Centralidade de Closeness
plt.figure(figsize=(10, 6))
sns.histplot(metrics_df['Closeness_Centralidade'], kde=True, color='purple')
plt.title("Distribuição da Centralidade de Closeness", fontsize=16)
plt.xlabel("Closeness", fontsize=14)
plt.ylabel("Frequência", fontsize=14)
plt.tight_layout()
plt.show()

# Distribuição da Centralidade de Grau
plt.figure(figsize=(10, 6))
sns.histplot(metrics_df['Grau_Centralidade'], kde=True, color='red')
plt.title("Distribuição da Centralidade de Grau", fontsize=16)
plt.xlabel("Grau de Centralidade", fontsize=14)
plt.ylabel("Frequência", fontsize=14)
plt.tight_layout()
plt.show()

# Distribuição do PageRank
plt.figure(figsize=(10, 6))
sns.histplot(pagerank_df['PageRank'], kde=True, color='orange')
plt.title("Distribuição do PageRank", fontsize=16)
plt.xlabel("PageRank", fontsize=14)
plt.ylabel("Frequência", fontsize=14)
plt.tight_layout()
plt.show()

print("\nAnálise concluída com sucesso.")
