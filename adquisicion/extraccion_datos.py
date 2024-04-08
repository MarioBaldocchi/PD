from extraccion_drive import procesar_archivo_info
from extraccion_drive import descargar_archivo_directo
from pathlib import Path

def extraccion_datos():
    """Saca los archivos de drive según archivos_info.txt"""
    path = Path.cwd()
    lista_links_archivos = procesar_archivo_info(Path(path, "archivos_info.txt"))
    rutas_archivos = []

    for link_archivo in lista_links_archivos:
        _, ruta_completa = descargar_archivo_directo(link_archivo[0], link_archivo[2], link_archivo[1])
        rutas_archivos.append(ruta_completa)

