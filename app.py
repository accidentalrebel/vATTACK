from flask import Flask, render_template, Markup, request
from plotly.callbacks import Points, InputDeviceState
import importlib
import plotly.graph_objects as go
import networkx as nx
import plotly.express as px
import json
import sys

print('[INFO] Starting...')

g_cti = importlib.import_module('mitre')
g_cti_src = g_cti.setup_cti_source()
print('[INFO] Finished setting up cti source.')

app = Flask(__name__)
app.debug = True

config = {'displayModeBar': False}

@app.route('/plot')
def plot():
    is_grouped = False
    
    if request.method == 'GET':
        can_group = request.args.get('can_group')
        if can_group:
            if can_group == 'false':
                is_grouped = False
            else:
                is_grouped = True
        search_text = request.args.get('search_text')

    print('search_text: ' + search_text)


    #g_technique_name = 'Access Token Manipulation'
    external_id = search_text
    print('[INFO] Fetching technique by id ' + external_id + '...')
    g_technique = g_cti.get_technique_by_external_id(g_cti_src, external_id)
    if not g_technique:
        g_technique_name = search_text
        print('[INFO] Fetching technique by name ' + g_technique_name + '...')

        g_technique = g_cti.get_technique_by_name(g_cti_src, g_technique_name)
    else:
        g_technique_name = g_cti.get_technique_name(g_cti_src, g_technique)
        
    g_technique_id = g_cti.get_technique_id(g_cti_src, g_technique)
    print('[INFO] Finished fetching technique: ' + g_technique_name)

    g_subs = g_cti.get_subtechnique_for_technique(g_cti_src, g_technique_id);
    print('[INFO] Finished fetching subtechniques.')
    g_groups = g_cti.get_groups_using_technique(g_cti_src, g_technique_id)
    print('[INFO] Finished fetching groups.')
    g_mitigations = g_cti.get_mitigations_for_technique(g_cti_src, g_technique_id)
    print('[INFO] Finished fetching mitigations.')
    g_malwares = g_cti.get_malware_for_technique(g_cti_src, g_technique_id)
    print('[INFO] Finished fetching malwares.')
    g_tools = g_cti.get_tool_for_technique(g_cti_src, g_technique_id)
    print('[INFO] Finished fetching tools.')

    points, state = Points(), InputDeviceState()

    G = nx.random_geometric_graph(50, 0.125)
    G = nx.Graph()

    G.add_node('main', name=g_technique_name, category='technique')
        
    i = 1
    if g_groups:
        for g in g_groups:
            group_name = g['object']['name']
            G.add_node(str(i), name=group_name, category='threat_group')
            G.add_edge('main', str(i))
            i+=1

    if g_mitigations:
        for m in g_mitigations:
            mitigation_name = m['object']['name']
            G.add_node(str(i), name=mitigation_name, category='prevention')
            G.add_edge('main', str(i))
            i+=1

    if g_malwares:
        for m in g_malwares:
            malware_name = m['object']['name']
            G.add_node(str(i), name=malware_name, category='malware')
            G.add_edge('main', str(i))
            i+=1

    if g_tools:
        for t in g_tools:
            tool_name = t['object']['name']
            G.add_node(str(i), name=tool_name, category='tool')
            G.add_edge('main', str(i))
            i+=1

    if g_subs:
        for s in g_subs:
            sub_name = s['object']['name']
            G.add_node(str(i), name=sub_name, category='technique')
            G.add_edge('main', str(i))
            i+=1

    fixed_pos = {'main':(0,0)}
    pos = nx.spring_layout(G, pos=fixed_pos, fixed=['main'])

    node_names = nx.get_node_attributes(G, 'name')
    node_categories = nx.get_node_attributes(G, 'category')
    
    if is_grouped:
        # Adjust positions for grouping
        for node in G.nodes:
            cat = node_categories[node]
            if cat == 'threat_group':
                pos[node][0] += 1
                pos[node][1] += 1
            elif cat == 'malware':
                pos[node][0] -= 1
                pos[node][1] += 1
            elif cat == 'tool':
                pos[node][0] -= 1
                pos[node][1] -= 1
            elif cat == 'prevention':
                pos[node][0] -= 0
                pos[node][1] += 1
            elif cat == 'technique' and node != 'main':
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

        if node == 'main':
            colors.append('#ffffff')
        elif cat == 'threat_group':
            colors.append('#ff0000')
        elif cat == 'prevention':
            colors.append('#d9ff00')
        elif cat == 'malware':
            colors.append('#ff8800')
        elif cat == 'tool':
            colors.append('#0352fc')            
        else:
            colors.append('#ff00ff')

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        hovertext=categories,
        text=names,
        textfont=dict(
            size=10,
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
            size=20,
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
                        text='VAtt&ck - Visual Att&ck',
                        showarrow=False,
                        xref='paper', yref='paper',
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    my_plot_div = fig.to_html(full_html=False, config=config)
    
    return render_template('plotter.html', plot_div=Markup(my_plot_div), is_grouped=str(is_grouped))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
