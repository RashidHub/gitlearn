from api import get_friends
from igraph import Graph, plot
import igraph

def get_network(users_ids, as_edgelist=True):
    edges = []
    if as_edgelist:
        for key1, id1 in enumerate(users_ids):
            try:
                friends_ids = get_friends(id1)
                for key2, id2 in enumerate(users_ids):
                    if id2 in friends_ids:
                        edges.append((key1, key2))
            except:
                pass

    if as_edgelist:
        return edges


def draw_graph(id_for_graph):
    friends = get_friends(id_for_graph, 'last_name')
    vertices = []
    for i in friends:
        vertices.append([i['last_name'], i['first_name']])
    edges = get_network(get_friends(id_for_graph), as_edgelist=True)
    g = Graph(vertex_attrs={"label": vertices},
              edges=edges, directed=False)
    g.simplify(multiple=True, loops=True)

    communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()

    N = len(vertices)
    visual_style = {}
    visual_style["vertex_size"] = 8
    visual_style["vertex_label"] = g.vs["label"]
    visual_style["bbox"] = (1200, 1000)
    visual_style["margin"] = 200
    visual_style["vertex_label_dist"] = 1
    visual_style["vertex_label_color"] = "black"
    visual_style["edge_color"] = "blue"
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=100000,
        area=N ** 2,
        repulserad=N ** 2)

    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    plot(g, **visual_style)

if __name__ == '__main__':
    draw_graph(559096549)
