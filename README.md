# Evaluación 2 - Visualización de Datos de Transporte
Autor: Cristopher San Martín

## Ejecución en Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip freeze > requirements.txt
.venv\Scripts\python.exe src/adquirir.py
.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace notebooks/evaluacion02.ipynb
```
Si la descarga falla, descargar manualmente el CSV oficial y guardarlo como `data/raw/operaciones.csv` sin modificarlo. El notebook genera las figuras y los hallazgos reales. El notebook fue ejecutado correctamente con datos oficiales, generando seis visualizaciones y los resultados del análisis.

## Estructura
`data/raw`: fuente; `data/processed`: datos preparados y excluidos; `notebooks`: análisis; `src`: descarga; `output/figures`: gráficos; `docs`: documentación.

## Contexto del proyecto
Cristopher San Martín | INACAP
## Problema y fuente
¿Cómo se distribuyen las operaciones aeroportuarias registradas en Chile según aeropuerto, tiempo y ámbito doméstico/internacional?
P1: ¿Qué aeropuertos concentran más operaciones? P2: ¿Cómo evolucionan mensualmente? P3: ¿Cómo difieren los ámbitos y la distribución de volúmenes mensuales?
H1: Las operaciones se concentran en pocos aeropuertos; hipótesis respaldada descriptivamente por los resultados.
Fuente: [Datos Abiertos](https://datos.gob.cl/dataset/operaciones-aeronaves), JAC, registros producidos por DGAC. [Diccionario](https://jac-mtt.github.io/jac-docs/docs/series/operaciones_aeroportuarias/). Licencia CC0. CSV: una fila por mes, aeropuerto y ámbito; medida: conteo de aterrizajes y despegues. No mide pasajeros ni vuelos únicos. Se excluyen sobrevuelos, operaciones militares/policiales y aeródromos sin administración DGAC según documentación. Parquet: bitácora individual, no equivalente al CSV agregado; no procede benchmark directo de formatos. CSV elegido por granularidad suficiente y tamaño manejable. Actualización mensual; cobertura efectiva desde enero de 2000 hasta octubre de 2026. Utilidad: planificación descriptiva de infraestructura, no inferencia causal.

## Perfilamiento y auditoría
Se analizaron 16.231 registros, cuatro variables, 70 aeropuertos y 322 meses. No se detectaron valores nulos, duplicados exactos, claves repetidas ni registros inválidos. Se conservaron todos los registros originales.

## Preparación y calidad
Se normalizan códigos con espacios y mayúsculas; se convierten meses y conteos. Se separan registros inválidos sin imputar operaciones. Los duplicados exactos se conservan inicialmente y se revisan: sin confirmación del productor no se presume que sean observaciones independientes ni se suman automáticamente claves repetidas. El análisis excluye claves ambiguas completas y reporta su magnitud. Los extremos válidos se conservan porque podrían representar actividad real.

## Variables derivadas y dimensionalidad
Año: extraído de fecha, comparación interanual. Mes: número de mes, estacionalidad. Trimestre: agrupación de tres meses, comparación temporal. Ámbito: etiqueta descriptiva de I/D. Jerarquía temporal año → trimestre → mes (mes dentro de año); aeropuerto es dimensión espacial nominal, no se infieren regiones. La clave compuesta identifica registros; cnt_operaciones es medida discreta aditiva de movimientos, no de vuelos únicos.

## Agregaciones y matriz de diseño
P1: aeropuerto + suma, barras ordenadas; pierde tiempo y ámbito. P2: mes calendario + suma, línea; pierde detalle por aeropuerto. P3: aeropuerto/mes/ámbito + suma, histograma y cajas; muestra dispersión y segmentación. Quinta figura: mes, conteo y ámbito por color. Benchmark P1: barras frente a puntos con misma selección y escala.

## Visualizaciones
Las barras parten de cero; la línea conserva meses ausentes como discontinuidades. Histograma y cajas conservan extremos, sin atribuirles error. El top 10 se declara explícitamente; el resto no se elimina del análisis global.

## Canales y benchmark
Mes → posición X (orden temporal); operaciones → posición Y (magnitud); ámbito → color (categorías). Agregar aeropuerto como otra línea dificultaría seguir cada serie; facetas serían preferibles.

| Criterio | Barras | Puntos |
|---|---|---|
| Claridad | Longitud directa | Posición directa |
| Precisión | Buena escala común | Buena escala común |
| Comparabilidad | Alta | Alta |
| Densidad | Menor | Mayor |
| Carga cognitiva | Baja | Baja |
| Utilidad | Ranking general | Comparación compacta |

Se eligen barras para audiencia general por familiaridad. Ambas muestran los mismos diez aeropuertos y escala desde cero.
## Validación
Gráfico 1: propósito ranking; audiencia planificación; sumas verificadas contra total; escala cero; color uniforme; etiquetas OACI; top 10 puede ocultar cola, por eso se publica ranking completo. Gráfico 2: propósito evolución; audiencia analistas; sumas mensuales validadas; escala cero, color único, meses sin registros no se imputan. Un mes parcial puede aparentar caída; no interpretar como descenso definitivo sin verificar cobertura. Ninguno mide pasajeros, demanda insatisfecha ni causalidad.

## Ética y conclusiones
Se optó por conservar extremos válidos y separar claves ambiguas, en vez de imputar o sumar automáticamente. La auditoría muestra cuántas filas se afectan. Excluir extremos reduciría artificialmente la dispersión; excluir claves ambiguas puede reducir el volumen informado. Se declara la exclusión, la cobertura y el top 10; se mantienen originales y excluidos para revisión. Las conclusiones cuantitativas se presentan en la sección de hallazgos y no se atribuyen causas. Las operaciones registradas permiten describir concentración, evolución y ámbito, pero no representan todo el tráfico nacional.

## Hallazgos

1. Concentración: SCEL registra 3,147,438 movimientos (29.34% del total). Figura 01. Permite priorizar revisión de infraestructura; no demuestra saturación.
2. Evolución: máximo mensual en 2024-01: 55,510 movimientos. Figura 02. Orienta revisión de capacidad estacional; cobertura desigual o meses parciales pueden afectar comparación.
3. Segmentación: Doméstico concentra 9,288,770 movimientos (86.60%). Figuras 04 y 05. Útil para distinguir ámbitos; no equivale a pasajeros ni a vuelos únicos.
Distribución: mediana 172.0, Q1 24.0, Q3 783.0, asimetría 3.49, observaciones sobre límite superior IQR: 1220. Los extremos se conservan; no son errores confirmados.
Hipótesis: los diez mayores representan 70.15% del total; esta proporción describe concentración sin establecer un umbral previo de prueba.
Cobertura efectiva: 2000-01 a 2026-10. Filas originales 16231, retenidas 16231.

## Autor
Cristopher San Martín

