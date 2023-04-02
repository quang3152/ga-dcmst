import networkx as nx


# print(nx.find_cycle(G))
# print(G)


# print()
def fix_cycle(nx_graph):
    while is_cycle(nx_graph):
        c = nx.find_cycle(nx_graph)
        rm_edge = c[1]
        nx_graph.remove_edge(c[1][0], c[1][1])
    return nx_graph


# print(fix_cycle(G))

def is_cycle(nx_graph):
    if not nx.is_tree(nx_graph) and nx.is_connected(nx_graph):
        return True
    else:
        return False


def make_connected(nx_graph):
    # Kiểm tra đồ thị ban đầu có liên thông không
    if nx.is_connected(nx_graph):
        return nx_graph

    # Lưu trữ các đỉnh được thăm trong quá trình duyệt BFS
    visited = set()

    # Duyệt qua tất cả các đỉnh của đồ thị
    for node in nx_graph.nodes():
        # Nếu đỉnh chưa được thăm, bắt đầu một quá trình BFS mới
        if node not in visited:
            # Tạo một đồ thị mới để lưu trữ thành phần liên thông hiện tại
            subgraph = nx.Graph()
            # Duyệt BFS để tìm tất cả các đỉnh thuộc cùng thành phần liên thông với đỉnh hiện tại
            queue = [node]
            while queue:
                current_node = queue.pop(0)
                if current_node not in visited:
                    visited.add(current_node)
                    subgraph.add_node(current_node)
                    queue.extend(nx_graph.neighbors(current_node))

            # Tìm các đỉnh kết nối giữa các thành phần liên thông
            for subnode in subgraph.nodes():
                for neighbor in nx_graph.neighbors(subnode):
                    # Nếu đỉnh kết nối không thuộc thành phần liên thông hiện tại
                    # tạo một cạnh để kết nối hai thành phần liên thông
                    if neighbor not in subgraph:
                        nx_graph.add_edge(subnode, neighbor)

    return nx_graph


# G = nx.Graph()
# G.add_edges_from(edges)
# G = make_connected(G)
# print(G.edges())


def make_graph_connected(G):
    # Tìm các thành phần liên thông của đồ thị
    subgraphs = list(nx.connected_components(G))
    print(subgraphs)

    # Nếu đồ thị đã liên thông, không cần thực hiện gì thêm
    if len(subgraphs) == 1:
        return G

    # Thêm các cạnh để kết nối các thành phần liên thông
    for i in range(len(subgraphs) - 1):
        nodes1 = subgraphs[i]
        nodes2 = subgraphs[i + 1]
        node1 = nodes1.pop()
        node2 = nodes2.pop()
        G.add_edge(node1, node2)

    return G


# edges = [(0, 1), (2, 3), (2, 4), (2, 5), (6, 7), (7, 8), (8, 6), (7, 2), (4, 8)]
edges = [(0, 1)]

G = nx.empty_graph(10)
G.add_edges_from(edges)
G = make_graph_connected(G)
print(G.edges)

print(fix_cycle(G).edges)
print(nx.is_tree(G))
