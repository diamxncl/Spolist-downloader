from youtubesearchpython import VideosSearch
from pytube import YouTube 
from spotipy.oauth2 import SpotifyClientCredentials
from pydub import AudioSegment
import os
import spotipy
import eyed3
import subprocess
import urllib.request

def getYTUrl(name):
    try:
        # Realizar la búsqueda de videos en YouTube
        videos_search = VideosSearch(name, limit=1)
        
        # Obtener los resultados de la búsqueda
        results = videos_search.result()
        
        # Extraer la URL del primer video encontrado
        if results['result']:
            first_video = results['result'][0]
            video_url = first_video['link']
            return video_url
        else:
            return "No se encontraron resultados para la canción especificada."
    except Exception as e:
        return f"Ocurrió un error: {str(e)}"

def downloadMp3(name, artists, album, image_url, playlist_name):
    try:
        # Obtener la URL de YouTube para la canción especificada
        url_youtube = getYTUrl(name)

        # url input from user
        yt = YouTube(url_youtube) 

        # Buscar la mejor calidad de audio disponible
        best_audio = yt.streams.filter(only_audio=True).order_by('abr').last()

        # check for destination to save file 
        destination = os.path.join('.', playlist_name)

        # create the directory if it does not exist
        os.makedirs(destination, exist_ok=True)

        # download the file 
        out_file = best_audio.download(output_path=destination) 

        # Renombrar el archivo descargado
        new_file = os.path.join(destination, name + '.mp3')

        # Convertir el archivo a formato MP3
        convert_to_mp3(out_file)

        # Agregar etiquetas ID3
        add_id3_tags(new_file, name, artists, album, image_url)  # Ajusta los argumentos según sea necesario
    except Exception as e:
        print(e)

def convert_to_mp3(file_path):
    # Obtener la extensión del archivo
    _, file_extension = os.path.splitext(file_path)

    # Verificar si el archivo es en formato MP3
    if file_extension.lower() == ".mp3":
        return  # El archivo ya está en formato MP3, no es necesario convertirlo
    
    # Verificar si el archivo es en formato webm
    if file_extension.lower() != ".webm":
        raise ValueError("El archivo no es un archivo WebM válido.")

    # Cargar el archivo de audio
    audio = AudioSegment.from_file(file_path, format="webm")

    # Definir la ruta de salida en formato MP3
    mp3_file_path = os.path.splitext(file_path)[0] + ".mp3"

    # Exportar el archivo en formato MP3
    audio.export(mp3_file_path, format="mp3")

    # Eliminar el archivo original
    os.remove(file_path)

def obtener_todas_las_canciones(playlist_id):
    # Credenciales de la aplicación de Spotify
    client_id = 'tu_client_id'
    client_secret = 'tu_client_secret'

    # Autenticación con Spotify
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Obtener información de la playlist
    canciones = []
    offset = 0
    total = None

    playlist = sp.playlist(playlist_id)
    playlist_name = playlist['name']
    while total is None or offset < total:
        playlist_info = sp.playlist_tracks(playlist_id, offset=offset)
        total = playlist_info['total']

        for item in playlist_info['items']:
            cancion = item['track']
            nombre_cancion = cancion['name']
            artistas = [artista['name'] for artista in cancion['artists']]
            album = cancion['album']['name']
            image_url = cancion['album']['images'][0]['url'] if cancion['album']['images'] else None
            duracion_ms = cancion['duration_ms']
            duracion_minutos = duracion_ms / 60000
            canciones.append({
                'nombre': nombre_cancion,
                'artistas': artistas,
                'album': album,
                'image_url': image_url,
                'duracion': duracion_minutos
            })

        offset += len(playlist_info['items'])

    return canciones, total, playlist_name

def add_id3_tags(file_path, name, artists, album, image_url):
    try:
        # Verificar que el archivo es un archivo MP3 válido
        if not file_path.endswith(".mp3"):
            raise ValueError("El archivo no es un archivo MP3 válido.")

        # Cargar el archivo de audio
        print(file_path)
        audiofile = eyed3.load(file_path)
        if audiofile is None:
            raise ValueError("No se pudo cargar el archivo de audio.")

        # Agregar información de la canción a las etiquetas ID3
        audiofile.tag = eyed3.id3.Tag()
        audiofile.tag.file_info = eyed3.id3.FileInfo(file_path)

        audiofile.tag.title = name
        audiofile.tag.album = album
        audiofile.tag.artist = ", ".join(artists)

        # Descargar la imagen de la portada y agregarla a las etiquetas ID3
        if image_url:
            image_data = urllib.request.urlopen(image_url).read()
            audiofile.tag.images.set(3, image_data, "image/jpeg", u"Description")
        
        # Guardar las etiquetas ID3
        audiofile.tag.save(version=eyed3.id3.ID3_V2_4, encoding='utf-8')
    except Exception as e:
        print(e)


# ID de la playlist que deseas obtener
playlist_id = input('Inserta la URL de la playlist: ')
info_playlist, totalCanciones, nombre = obtener_todas_las_canciones(playlist_id)

directory = os.path.join("songs", nombre)
os.mkdir(directory)

# Mostrar información de las canciones en la playlist
for i, cancion in enumerate(info_playlist, start=1):
    print(f"Descargando {i}/{totalCanciones}: {cancion['nombre']} - {', '.join(cancion['artistas'])}")
    downloadMp3(cancion['nombre'], cancion['artistas'], cancion['album'], cancion['image_url'], directory)
