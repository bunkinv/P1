import sys
import spotipy
import spotipy.util as sutil
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'fec2cd5b78be49489d8bb3e70343d805'
secret_id = '1213ece49c214e88b54b6b606dcea268'

scope = 'user-library-read'

# scope registration

if len(sys.argv) > 1:
	username = sys.argv[1]
else:
	print("Usage: %s username" % (sys.argv[0],))
	sys.exit()

token = sutil.prompt_for_user_token(username, scope)

if token:
	sp = spotipy.Spotify(auth=token)
	results = sp.current_user_saved_tracks()
	for item in results['items']:
		track = item['track']
		print(track['name'] + ' - ' + track['artists'][0]['name'])
else:
	print("Can't get token for", username)

# login

client_credentials_manager = SpotifyClientCredentials(client_id, secret_id)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists('117183927')
while playlists:
	for i, playlist in enumerate(playlists['items']):
		print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'], playlist['name']))
	if playlists['next']:
		playlists = sp.next(playlists)
	else:
		playlists = None
