# https://graphviz.org/docs/layouts/writing-layout-plugins/

import json
import networkx as nx
import matplotlib.pyplot as plt

def show_graph(d, root=None, seed=42, node_size=900, font_size=10, figsize=(12, 8), prog='twopi', debug=False): #
    G = nx.DiGraph()
    traverse_dict(G, None, d, debug=debug)
#     pos = nx.spring_layout(G, iterations=1, seed=seed)
    pos = nx.nx_agraph.graphviz_layout(G, prog=prog, root=root)
#     pos = nx.nx_pydot.graphviz_layout(G, prog=prog, root=root)
    
    plt.figure(figsize=figsize)  # Установка размера изображения
    plt.title(prog)
    nx.draw(G, pos,
            node_size=node_size,
            alpha=0.6,
            font_size=font_size,
            with_labels=True,
            arrows=True)
    # draw nodes, coloring by rtt ping time
#     options = {"with_labels": False, "alpha": 0.5, "node_size": 15}
#     nx.draw(G, pos, node_color=[G.rtt[v] for v in G], **options)

def add_edge_math(G, f, t, weight=1):
    G.add_edge(f, t, weight=1)

def add_edge(G, f, t, weight=1):
    new_line = '\n'
    G.add_edge(fr"{f.replace(' ',new_line)}", fr"{t.replace(' ',new_line)}", weight=1)


def load(lecture):
    with open('kg/'+lecture+'.json', 'r') as fp:
        return json.load(fp)
def save(d, lecture):
    with open('kg/'+lecture+'.json', 'w') as fp:
        json.dump(d, fp, ensure_ascii=False, indent='\t')

# with open('kg_0306.json', 'r') as fp:
#     d = json.load(fp)
def showg(d, root='None',  figsize=(12, 7), font_size=11, prog='sfdp'):
    show_graph(d, root, node_size=1900, 
              font_size=font_size, debug=False, figsize=figsize, prog=prog)
    
def append(d, key, val):
    if not key in d:
        d[key] = []
    if type(val) is list:
        d[key].extend(val)
        d[key] = list(set(d[key]))
    else:
        d[key].append(val)
        d[key] = list(set(d[key]))
    

def traverse_dict(G, pkey, dct, lvl=0, debug=False):
    if pkey is None:
        for k, v in dct.items():
            if debug:print( f'0:{lvl}>{k},{v}')
            traverse_dict(G, k, v, lvl+1, debug=debug)
        return 
    if not(type(dct) is dict): 
        if debug:print('not dict', pkey, dct)
        for v in dct:
            if debug:print("".join(["\t"]*lvl)+f'{lvl}-[{pkey}], [{v}]')
            add_edge(G, pkey, v,1)
            
#         print('return')
        return;

    for k, v in dct.items():
        if debug:print("".join(["\t"]*lvl)+f'{lvl}+[{pkey}], [{k}]')
        add_edge(G, pkey, k, weight=1)
        if type(v) is dict:
            traverse_dict(G, k, v, lvl+1, debug=debug)
        else:
            traverse_dict(G, k, v, lvl+1, debug=debug)
            