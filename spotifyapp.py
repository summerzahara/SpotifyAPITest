# pip3 install flask spotipy

import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect

#initiate Flask App
app = Flask(__name__)

app.config["SESSION_COOKIE_NAME"] = "Spotify Cookie"
app.secret_key = "jdjsdhj737337jfjfjf#%"
TOKEN_INFO = "token_info"

@app.route("/")
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route("/redirect")
def redirect_page():
    session.clear()
    code = request.args.get("code")
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for("display_fav", external=True))

@app.route("/displayFav")
def display_fav():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect("/")
  
    sp = spotipy.Spotify(auth=token_info["access_token"])
    top_tracks = sp.current_user_top_tracks(10,0,"short_term")
    for track in top_tracks['items']:
        print('track    : ' + track['name'])
        print('audio    : ' + track['preview_url'])
        print('cover art: ' + track['album']['images'][0]['url'])
        print()
    return("Success")

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for("login", external=False))
    now = int(time.time())
    is_expired = token_info["expires_at"] - now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info["refesh_token"])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = "64eb0ca0a3644f19b2152d38843167e0",
        client_secret = "18607f1d3c5a45c9a46c48e5fe5242fe",
        redirect_uri = url_for('redirect_page', _external= True),
        scope = "user-top-read"
    )

app.run(debug=True)