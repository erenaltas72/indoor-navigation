from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings

# BeautifulSoup uyarısını gizle
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def get_nodes_from_layer(svg_path, layer_name):
    """
    Belirli bir katmandaki tüm daire ve dikdörtgenlerin ID ve koordinatlarını döndürür.
    """
    nodes_with_ids = {}
    isimsiz_dugum_sayaci = 1
    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'lxml-xml')
    except FileNotFoundError:
        return {}

    layer = soup.find('g', {'id': layer_name})
    if not layer:
        return {}

    elements = layer.find_all(['circle', 'rect'])
    
    for element in elements:
        element_id = element.get('id')
        
        if not element_id:
            element_id = f'isimsiz_{layer_name}_dugumu_{isimsiz_dugum_sayaci}'
            isimsiz_dugum_sayaci += 1
            
        x, y = 0, 0
        if element.name == 'circle':
            x = float(element.get('cx', 0))
            y = float(element.get('cy', 0))
        elif element.name == 'rect':
            x = float(element.get('x', 0)) + float(element.get('width', 0)) / 2
            y = float(element.get('y', 0)) + float(element.get('height', 0)) / 2
        
        nodes_with_ids[element_id] = {'x': x, 'y': y}
        
    return nodes_with_ids

# Kullanım örneği
svg_dosyasi = "harita - nodlu.svg"

# Farklı katmanlardaki düğümleri al
kapi_dugumleri = get_nodes_from_layer(svg_dosyasi, "kapılar")
koridor_dugumleri = get_nodes_from_layer(svg_dosyasi, "koridorlar")
oda_dugumleri = get_nodes_from_layer(svg_dosyasi, "odalar")

# Tüm düğümleri tek bir sözlükte birleştir
dugumler_dict = {**kapi_dugumleri, **koridor_dugumleri, **oda_dugumleri}

# Çıktıyı bir metin dosyasına yaz
with open("dugum_listesi.txt", "w", encoding="utf-8") as output_file:
    output_file.write("--- Kapı Düğümleri ---\n")
    for dugum_id, dugum_coords in kapi_dugumleri.items():
        output_file.write(f"ID: {dugum_id}, x={dugum_coords['x']:.2f}, y={dugum_coords['y']:.2f}\n")

    output_file.write("\n--- Koridor Düğümleri ---\n")
    for dugum_id, dugum_coords in koridor_dugumleri.items():
        output_file.write(f"ID: {dugum_id}, x={dugum_coords['x']:.2f}, y={dugum_coords['y']:.2f}\n")

    output_file.write("\n--- Oda Düğümleri ---\n")
    for dugum_id, dugum_coords in oda_dugumleri.items():
        output_file.write(f"ID: {dugum_id}, x={dugum_coords['x']:.2f}, y={dugum_coords['y']:.2f}\n")

    output_file.write(f"\nToplam '{len(dugumler_dict)}' düğüm bulundu.")
    output_file.write(f" (Kapı: {len(kapi_dugumleri)}, Koridor: {len(koridor_dugumleri)}, Oda: {len(oda_dugumleri)})")

print("Düğüm listesi 'dugum_listesi.txt' dosyasına kaydedildi.")