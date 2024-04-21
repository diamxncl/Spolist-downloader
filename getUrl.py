from youtubesearchpython import VideosSearch
from pytube import YouTube 
from spotipy.oauth2 import SpotifyClientCredentials

import os
import spotipy

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

def downloadMp3(name, playlist_name):
    try:
        # Obtener la URL de YouTube para la canción especificada
        url_youtube = getYTUrl(name)

        # url input from user
        yt = YouTube(url_youtube) 

        # Buscar la mejor calidad de audio disponible
        best_audio = yt.streams.filter(only_audio=True).order_by('abr').last()

        # check for destination to save file 
        destination = './' + playlist_name

        # download the file 
        out_file = best_audio.download(output_path=destination) 

        # save the file with the specified name + ".mp3"
        new_file = os.path.join(destination, name + '.mp3')
        os.rename(out_file, new_file)
    except Exception as e:
        print(e)

def obtener_todas_las_canciones(playlist_id):
    # Credenciales de la aplicación de Spotify
    client_id = 'cd4d4bfdc11044e6a5cc10763adad094'
    client_secret = 'be8637dc04fd45ad9f0d757a64364c1d'

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
            duracion_ms = cancion['duration_ms']
            duracion_minutos = duracion_ms / 60000
            canciones.append({
                'nombre': nombre_cancion,
                'artistas': artistas,
                'album': album,
                'duracion': duracion_minutos
            })

        offset += len(playlist_info['items'])

    return canciones, total, playlist_name

# ID de la playlist que deseas obtener
playlist_id = input('Insert the playlist URL: ')
info_playlist, totalCanciones, nombre = obtener_todas_las_canciones(playlist_id)

directory = os.path.join("songs", nombre)
os.mkdir(directory)

song_id = 0

# Mostrar información de las canciones en la playlist
for i, cancion in enumerate(info_playlist, start=1):
    print(f"Descargando {i}/{totalCanciones}: {cancion['nombre']} - {', '.join(cancion['artistas'])}")
    downloadMp3(f"{song_id} - {cancion['nombre']} - {', '.join(cancion['artistas'])}", directory)
    song_id += 1