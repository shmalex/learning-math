import matplotlib.pyplot as plt
import networkx as nx

def show_graph(d, root=None, seed=42, node_size=900, font_size=10, debug=False):
    G = nx.DiGraph()
    traverse_dict(G, None, d, debug=debug)
#     pos = nx.spring_layout(G, iterations=1, seed=seed)
    pos = nx.nx_agraph.graphviz_layout(G, prog="twopi", root=root)
    nx.draw(G, pos,
            node_size=node_size,
            alpha=0.6,
            font_size=font_size,
            with_labels=True,
            arrows=True)
    # draw nodes, coloring by rtt ping time
#     options = {"with_labels": False, "alpha": 0.5, "node_size": 15}
#     nx.draw(G, pos, node_color=[G.rtt[v] for v in G], **options)


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
            G.add_edge(pkey.replace(' ','\n'), v.replace(' ','\n'), weight=1)
            
#         print('return')
        return;

    for k, v in dct.items():
        if debug:print("".join(["\t"]*lvl)+f'{lvl}+[{pkey}], [{k}]')
        G.add_edge(pkey.replace(' ','\n'), k.replace(' ','\n'), weight=1)
        if type(v) is dict:
            traverse_dict(G, k, v, lvl+1, debug=debug)
        else:
            traverse_dict(G, k, v, lvl+1, debug=debug)
            