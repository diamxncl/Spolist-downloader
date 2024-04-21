import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

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

    return canciones

# ID de la playlist que deseas obtener
playlist_id = 'https://open.spotify.com/playlist/6paEKqwwNmMX9HzqUTKT2J?si=f0b9f6fd56c44c01'
info_playlist = obtener_todas_las_canciones(playlist_id)

# Mostrar información de las canciones en la playlist
for i, cancion in enumerate(info_playlist, start=1):
    print(f"{i}. {cancion['nombre']} - {', '.join(cancion['artistas'])} ({cancion['album']}) - Duración: {cancion['duracion']} minutos")
