import json
import matplotlib.pyplot as plt
import networkx as nx
import math

# JSON dosyası yükleme
with open("map.json", "r") as f:
    data = json.load(f)

nodes = data["nodes"]
paths = data["paths"]

# Graph oluşturma
G = nx.Graph()
for i, node in enumerate(nodes):
    G.add_node(i, pos=(node["x"], node["y"]))

for path in paths:
    a, b = path
    x1, y1 = nodes[a]["x"], nodes[a]["y"]
    x2, y2 = nodes[b]["x"], nodes[b]["y"]
    weight = math.dist((x1, y1), (x2, y2))
    G.add_edge(a, b, weight=weight)

# Görsel hazırlama
fig, ax = plt.subplots()
img = plt.imread("map.jpg")
ax.imshow(img, extent=[0, img.shape[1], img.shape[0], 0])

# Başlangıç ve hedefi tutan değişkenler
start_node = None
end_node = None
route_line = None

# En yakın düğümü bulan fonksiyon
def closest_node(x, y):
    return min(G.nodes, key=lambda i: math.dist((x, y), (nodes[i]["x"], nodes[i]["y"])))

# Tıklama eventi
def on_click(event):
    global start_node, end_node, route_line
    if event.inaxes != ax:
        return
    
    x, y = event.xdata, event.ydata
    clicked_node = closest_node(x, y)
    
    if start_node is None:
        start_node = clicked_node
        print(f"Başlangıç noktası seçildi: {start_node}")
    elif end_node is None:
        end_node = clicked_node
        print(f"Hedef seçildi: {end_node}")
        path = nx.shortest_path(G, start_node, end_node, weight="weight")
        coords = [(nodes[p]["x"], nodes[p]["y"]) for p in path]
        xs, ys = zip(*coords)
        route_line, = ax.plot(xs, ys, color="red", linewidth=2)
        fig.canvas.draw()

# Haritayı sıfırlama fonksiyonu
def reset(event):
    global start_node, end_node, route_line
    start_node = None
    end_node = None
    if route_line:
        route_line.remove()
        route_line = None
    fig.canvas.draw()
    print("Harita sıfırlandı!")

# Eventleri bağla
fig.canvas.mpl_connect("button_press_event", on_click)

# Sıfırlama tuşu (klavyeden "r" harfine basılınca sıfırlanır)
def on_key(event):
    if event.key == "r":
        reset(event)

fig.canvas.mpl_connect("key_press_event", on_key)

plt.show()
