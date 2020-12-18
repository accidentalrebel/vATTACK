from flask import Flask, render_template, Markup, request
from plotly.callbacks import Points, InputDeviceState
import importlib
import plotly.graph_objects as go
import networkx as nx
import plotly.express as px
import json
import sys

cti = importlib.import_module('taxii')

app = Flask(__name__)
app.debug = True

config = {'displayModeBar': False}

@app.route('/', methods=['GET', 'POST'])
def index():
    cti_src = cti.setup_cti_source()
    technqiue_id = cti.get_groups(cti_src)
    return 'true' + str(technqiue_id)
    sys.exit()
    can_group = False
    
    if request.method == 'POST':
        group = request.form.get('group')
        if group == 'False':
            can_group = True
        else:
            can_group = False

    points, state = Points(), InputDeviceState()

    G = nx.random_geometric_graph(50, 0.125)
    G = nx.Graph()

    G.add_node("A", name="T1105", category="technique")
    G.add_node("B", name="APT-C-36", category='threat_group')
    G.add_node("C", name="APT18", category='threat_group')
    G.add_node("D", name="APT28 ", category='threat_group')
    G.add_node("E", name="Network Intrusion Prevention", category='prevention')
    G.add_node("F", name="Auditcred", category='malware')
    G.add_node("G", name="BadPatch", category='malware')
    G.add_node("H", name="T1105", category="technique")
    G.add_node("I", name="APT-C-36", category='threat_group')
    G.add_node("J", name="APT18", category='threat_group')
    G.add_node("K", name="APT28 ", category='threat_group')
    G.add_node("L", name="Network Intrusion Prevention", category='prevention')
    G.add_node("M", name="Auditcred", category='malware')
    G.add_node("N", name="BadPatch", category='malware')
    G.add_node("XA", name="T1105", category="technique")
    G.add_node("XB", name="APT-C-36", category='threat_group')
    G.add_node("XC", name="APT18", category='threat_group')
    G.add_node("XD", name="APT28 ", category='threat_group')
    G.add_node("XE", name="Network Intrusion Prevention", category='prevention')
    G.add_node("XF", name="Auditcred", category='malware')
    G.add_node("XG", name="BadPatch", category='malware')
    G.add_node("XH", name="T1105", category="technique")
    G.add_node("XI", name="APT-C-36", category='threat_group')
    G.add_node("XJ", name="APT18", category='threat_group')
    G.add_node("XK", name="APT28 ", category='threat_group')
    G.add_node("XL", name="Network Intrusion Prevention", category='prevention')
    G.add_node("XM", name="Auditcred", category='malware')
    G.add_node("XN", name="BadPatch", category='malware')

    G.add_edge('A', 'B')
    G.add_edge('A', 'C')
    G.add_edge('A', 'D')
    G.add_edge('A', 'E')
    G.add_edge('A', 'F')
    G.add_edge('A', 'G')
    G.add_edge('A', 'H')
    G.add_edge('A', 'I')
    G.add_edge('A', 'J')
    G.add_edge('A', 'K')
    G.add_edge('A', 'L')
    G.add_edge('A', 'M')
    G.add_edge('A', 'N')
    G.add_edge('A', 'XA')
    G.add_edge('A', 'XB')
    G.add_edge('A', 'XC')
    G.add_edge('A', 'XD')
    G.add_edge('A', 'XE')
    G.add_edge('A', 'XF')
    G.add_edge('A', 'XG')
    G.add_edge('A', 'XH')
    G.add_edge('A', 'XI')
    G.add_edge('A', 'XJ')
    G.add_edge('A', 'XK')
    G.add_edge('A', 'XL')
    G.add_edge('A', 'XM')
    G.add_edge('A', 'XN')
    G.add_edge('C', 'D')
    # G.add_edge('B', 'D')
    # G.add_edge('C', 'D')

    fixed_pos = {'A':(0,0)}
    pos = nx.spring_layout(G, pos=fixed_pos, fixed=['A']) #, 'B'])

    node_names = nx.get_node_attributes(G, "name")
    node_categories = nx.get_node_attributes(G, "category")
    
    if can_group:
        # Adjust positions for grouping
        for node in G.nodes:
            cat = node_categories[node]
            if cat == 'threat_group':
                pos[node][0] += 1
                pos[node][1] += 1
            elif cat == 'malware':
                pos[node][0] -= 1
                pos[node][1] += 1
            elif cat == 'prevention':
                pos[node][0] -= 1
                pos[node][1] -= 1
            elif cat == 'technique' and node != 'A':
                pos[node][0] += 1
                pos[node][1] -= 1

    # Edges
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

    for node in G.nodes:
        names.append(node_names[node])
        # names.append(node)
        x,y = pos[node]
        node_x.append(x)
        node_y.append(y)

        cat = node_categories[node]
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
            showscale=False,
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
                    # title='<br>VAtt&ck made with Python',
                    # titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="VAtt&ck - Visual Att&ck",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    
    my_plot_div = fig.to_html(full_html=False, config=config)
    return render_template('index.html', div_placeholder=Markup(my_plot_div), grouped=can_group)
