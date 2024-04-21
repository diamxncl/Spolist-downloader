import eyed3

file_path = "/mnt/c/Users/bzddi/OneDrive - CFOP Puenteuropa/Programación/Python/Proyectos/yt-video-tools/songs/Himnos/It Wasn't Me - Shaggy, Rik Rok.mp3"

# Intenta cargar el archivo manualmente
audiofile = eyed3.load(file_path)
if audiofile is None:
    print("No se pudo cargar el archivo de audio.")
else:
    print("Archivo de audio cargado correctamente.")