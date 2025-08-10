import networkx as nx
import math
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings

# BeautifulSoup uyarısını gizle
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def get_nodes_from_layer(svg_path, layer_name):
    """
    Belirli bir katmandaki tüm daire ve dikdörtgenlerin koordinatlarını döndürür.
    
    Args:
        svg_path (str): SVG dosyasının yolu.
        layer_name (str): Düğümlerin bulunduğu katmanın adı.
        
    Returns:
        list: Her bir düğümün x ve y koordinatlarını içeren bir sözlük listesi.
    """
    nodes = []
    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'lxml-xml')
    except FileNotFoundError:
        print(f"Hata: '{svg_path}' dosyası bulunamadı.")
        return []

    layer = soup.find('g', {'id': layer_name})
    if not layer:
        print(f"Hata: SVG dosyasında '{layer_name}' adında bir katman bulunamadı.")
        return []

    # Hem daireleri hem de dikdörtgenleri bulmak için kod güncellendi
    elements = layer.find_all(['circle', 'rect'])
    
    for element in elements:
        x, y = 0, 0
        if element.name == 'circle':
            x = float(element.get('cx', 0))
            y = float(element.get('cy', 0))
        elif element.name == 'rect':
            # Dikdörtgenin merkez koordinatlarını hesapla
            x = float(element.get('x', 0)) + float(element.get('width', 0)) / 2
            y = float(element.get('y', 0)) + float(element.get('height', 0)) / 2
        
        nodes.append({'x': x, 'y': y})
    return nodes

def calculate_distance(node1, node2):
    """İki düğüm arasındaki Öklid mesafesini hesaplar."""
    return math.sqrt((node2['x'] - node1['x'])**2 + (node2['y'] - node1['y'])**2)

# Kullanım örneği
svg_dosyasi = "harita - nodlu.svg"

# Farklı katmanlardaki düğümleri al
kapi_dugumleri = get_nodes_from_layer(svg_dosyasi, "kapılar")
koridor_dugumleri = get_nodes_from_layer(svg_dosyasi, "koridorlar")
oda_dugumleri = get_nodes_from_layer(svg_dosyasi, "odalar")

# Tüm düğümleri tek bir sözlükte birleştir ve benzersiz ID'ler atayın
dugumler_dict = {}

for i, dugum in enumerate(kapi_dugumleri):
    dugumler_dict[f'kapi_dugumu_{i+1}'] = dugum
for i, dugum in enumerate(koridor_dugumleri):
    dugumler_dict[f'koridor_dugumu_{i+1}'] = dugum
for i, dugum in enumerate(oda_dugumleri):
    dugumler_dict[f'oda_dugumu_{i+1}'] = dugum

print(f"Toplam '{len(dugumler_dict)}' düğüm bulundu.")
print(f"Kapı düğümleri: {len(kapi_dugumleri)}, Koridor düğümleri: {len(koridor_dugumleri)}, Oda düğümleri: {len(oda_dugumleri)}")

# ... (Kalan kısım aynı) ...
# BURAYI SİZİN ELLE DOLDURMANIZ GEREKİYOR
baglantilar = [
    # Örnek: ('oda_dugumu_1', 'kapi_dugumu_1')
    # Örnek: ('kapi_dugumu_1', 'koridor_dugumu_5')
    # Örnek: ('koridor_dugumu_1', 'koridor_dugumu_2')
]

G = nx.Graph()
for dugum_id, coords in dugumler_dict.items():
    G.add_node(dugum_id, pos=(coords['x'], coords['y']))
for dugum_a, dugum_b in baglantilar:
    if dugum_a in dugumler_dict and dugum_b in dugumler_dict:
        node_a = dugumler_dict[dugum_a]
        node_b = dugumler_dict[dugum_b]
        mesafe = calculate_distance(node_a, node_b)
        G.add_edge(dugum_a, dugum_b, weight=mesafe)

print(f"Graf düğüm sayısı: {G.number_of_nodes()}")
print(f"Graf kenar sayısı: {G.number_of_edges()}")

baslangic_dugumu = 'oda_dugumu_1'
bitis_dugumu = 'oda_dugumu_2'

if G.has_node(baslangic_dugumu) and G.has_node(bitis_dugumu):
    if nx.has_path(G, baslangic_dugumu, bitis_dugumu):
        en_kisa_yol = nx.dijkstra_path(G, source=baslangic_dugumu, target=bitis_dugumu)
        mesafe = nx.dijkstra_path_length(G, source=baslangic_dugumu, target=bitis_dugumu)
        print(f"\nEn kısa yol: {en_kisa_yol}")
        print(f"Toplam mesafe: {mesafe:.2f} birim")
    else:
        print("\nBelirtilen düğümler arasında bir yol bulunamadı. Bağlantılar listesini kontrol edin.")
else:
    print("\nBaşlangıç veya bitiş düğümü graf üzerinde bulunamadı. Düğüm adlarını kontrol edin.")