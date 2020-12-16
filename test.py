from plotly.graph_objs import Scatter, Layout
import plotly.graph_objects as go
import plotly
import networkx as nx
import sys

G = nx.random_geometric_graph(50, 0.125)
G = nx.Graph()

G.add_node("A", name="T1105", category="technique")
G.add_node("B", name="APT-C-36", category='threat_group')
G.add_node("C", name="APT18", category='threat_group')
G.add_node("D", name="APT28 ", category='threat_group')
G.add_node("E", name="Network Intrusion Prevention", category='prevention')
G.add_node("F", name="Auditcred", category='malware')
G.add_node("G", name="BadPatch", category='malware')

G.add_edge('A', 'B')
G.add_edge('A', 'C')
G.add_edge('A', 'D')
G.add_edge('A', 'E')
G.add_edge('A', 'F')
G.add_edge('A', 'G')
G.add_edge('C', 'D')
# G.add_edge('B', 'D')
# G.add_edge('C', 'D')

fixed_pos = {'A':(0,0)}
pos = nx.spring_layout(G, pos=fixed_pos, fixed=['A']) #, 'B'])
print(pos)

edge_x = []
edge_y = []
for edge in G.edges:
    x0,y0 = pos[edge[0]]
    x1,y1 = pos[edge[1]]
    
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='#888'),
    hoverinfo='none',
    mode='lines')

## NODES

node_x = []
node_y = []
names = []
colors = []
categories = []

node_names = nx.get_node_attributes(G, "name")
node_categories = nx.get_node_attributes(G, "category")
print(node_names)

for node in G.nodes:
    print(node)
    names.append(node_names[node[0]])
    # names.append(node)
    x,y = pos[node[0]]
    node_x.append(x)
    node_y.append(y)

    cat = node_categories[node[0]]
    categories.append(cat)
    
    if cat == 'threat_group':
        colors.append('#ff0000')
    elif cat == 'prevention':
        colors.append('#d9ff00')
    elif cat == 'malware':
        colors.append('#ff8800')
    else:
        colors.append('#ff00ff')

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    hoverinfo='text',
    hovertext=categories,
    text=names,
    textfont=dict(
        size=16,
        color='#000000'
        ),
    textposition='top center',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=colors,
        size=40,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=4))

## DRAW

fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=True,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
fig.show()


