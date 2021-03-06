from flask import render_template, request
from app import app
import os, os.path
import vlc

music_folder = "/home/pi/music"
now_playing = {}
instance = vlc.Instance('--aout=alsa')
player = instance.media_list_player_new()

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        handle_form(request.form)
    artists = list_folders(music_folder)
    return render_template('index.html', artists=artists, now_playing=now_playing)
    
@app.route('/artist/<artist>', methods=['POST', 'GET'])
def show_artist(artist):
    if request.method == 'POST':
        handle_form(request.form)
    albums = list_folders(os.path.join(music_folder, artist))
    return render_template('artist.html', artist=artist, albums=albums, now_playing=now_playing)
    
@app.route('/album/<artist>/<album>', methods=['POST', 'GET'])
def show_album(artist, album):
    if request.method == 'POST':
        handle_form(request.form)
    tracks = list_tracks(artist, album)
    return render_template('album.html', album=album, tracks=tracks, artist=artist, 
                           now_playing=now_playing)

@app.route('/shutdown', methods=['POST', 'GET'])
def show_shutdown():
    if request.method == 'POST':
        do_shutdown()
        shutting_down = True
    else:
        shutting_down = False
    return render_template('shutdown.html', shutting_down=shutting_down)
    
def list_folders(folder):
    items = os.listdir(folder)
    r = [item for item in items if os.path.isdir(os.path.join(folder, item))]
    return sorted(r)
    
def list_tracks(artist, album):
    items = os.listdir(os.path.join(music_folder, artist, album))
    r = [item[:-4] for item in items if item.endswith(".mp3")]
    return sorted(r)
    
def handle_form(form):
    if form["action"] == "Stop":
        now_playing.clear()
        stop_player()
    elif form["action"] == "Pause":
        pause_player()
    elif form["action"] == "Skip":
        skip_player()
    elif form["action"] == "Play":
        now_playing.clear()
        now_playing["artist"] = form["artist"]
        now_playing["album"] = form["album"]
        now_playing["track"] = form["track"]
        play_player(now_playing)
        
def play_player(info):
    stop_player()
    tracks = list_tracks(info["artist"], info["album"])
    start = tracks.index(info["track"])
    playlist = instance.media_list_new()
    for track in tracks[start:]:
        playlist.add_media(os.path.join(music_folder, 
                                        info["artist"], 
                                        info["album"], 
                                        track + ".mp3"))
    player.set_media_list(playlist)
    player.play()
        
def skip_player():
    if player.is_playing():
        player.next()
        
def stop_player():
    state = player.get_state()
    if state == vlc.State.Playing or state == vlc.State.Paused:
        player.stop()
        
def pause_player():
    state = player.get_state()
    if state == vlc.State.Playing or state == vlc.State.Paused:
        player.pause()

def do_shutdown():
    os.system("/usr/bin/sudo /sbin/shutdown")