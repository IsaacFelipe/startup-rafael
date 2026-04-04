import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.buscar_musica_ou_hino import buscar_musica_no_youtube
from tools.buscar_noticia_personalizada import buscar_noticia_personalizada

try:
    print("Testing buscar_musica_no_youtube:")
    res = buscar_musica_no_youtube.invoke({"musica": "Harpa crista 15"})
    print(res)
except Exception as e:
    print("Error:", e)

try:
    print("\nTesting buscar_noticia_personalizada:")
    res = buscar_noticia_personalizada.invoke({"categoria": "futebol", "regiao": "são paulo", "tempo": "hoje"})
    print(res)
except Exception as e:
    print("Error:", e)
