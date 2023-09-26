import requests
from django.shortcuts import render
from myapp.models import SpotifyToken
from django.shortcuts import redirect
from django.http import HttpResponse
import os

# Import the login_required decorator
from django.contrib.auth.decorators import login_required

@login_required
def authorize_spotify(request):
    client_id = os.getenv('CLIENT_ID')
    redirect_uri = "http://localhost/"  # placeholder uri
    scopes = 'user-read-email user-library-read playlist-read-private'
    
    spotify_authorize_url = f"https://accounts.spotify.com/authorize/?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scopes}"

    return redirect(spotify_authorize_url)

@login_required
def spotify_callback(request):
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = "http://localhost/"  # placeholder uri

    authorization_code = request.GET.get('code')

    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    token_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        refresh_token = token_data['refresh_token']
        token_expiry = token_data['expires_in']

        user = request.user  # Assuming you have implemented user authentication

        # Create an instance of SpotifyToken and store the tokens
        spotify_token, _ = SpotifyToken.objects.get_or_create(user=user)
        spotify_token.store_tokens(access_token, refresh_token, token_expiry)

        return redirect('spotify_data_page')

    else:
        return HttpResponse("Error: Unable to obtain access token from Spotify.")
    
def my_view_function(request):
    # Your view logic goes here
    return render(request, 'my_template.html', {})

def landing_page(request):
    return render(request, 'landing_page.html')