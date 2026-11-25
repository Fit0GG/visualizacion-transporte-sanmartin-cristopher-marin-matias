from pathlib import Path
from urllib.request import urlretrieve
p=Path(__file__).resolve().parents[1]/"data/raw/operaciones.csv"
p.parent.mkdir(parents=True,exist_ok=True)
if not p.exists(): urlretrieve('https://datos.gob.cl/dataset/d5fac3ed-01c7-43f0-9dc4-8970566bc059/resource/2b7f3fbd-8be8-45e6-8ef5-64eea097528b/download/operaciones-aeropuertos.csv',p)
print(p)
