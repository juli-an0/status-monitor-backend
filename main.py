from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)

# Funktion: Discord-Status
def get_discord_status():
    try:
        page = requests.get('https://status.discord.com', timeout=5)
        soup = BeautifulSoup(page.content, 'html.parser')
        status = soup.find('span', class_='component-status').text.strip()
        return {'service': 'Discord', 'status': status}
    except:
        return {'service': 'Discord', 'status': 'Fehler'}

# Funktion: GitHub-Status
def get_github_status():
    try:
        page = requests.get('https://www.githubstatus.com/', timeout=5)
        soup = BeautifulSoup(page.content, 'html.parser')
        status = soup.find('span', class_='component-status').text.strip()
        return {'service': 'GitHub', 'status': status}
    except:
        return {'service': 'GitHub', 'status': 'Fehler'}

# Funktion: Zoom-Status
def get_zoom_status():
    try:
        page = requests.get('https://status.zoom.us/', timeout=5)
        soup = BeautifulSoup(page.content, 'html.parser')
        status = soup.find('span', class_='component-status').text.strip()
        return {'service': 'Zoom', 'status': status}
    except:
        return {'service': 'Zoom', 'status': 'Fehler'}

# Funktion: Twitter-Status
def get_twitter_status():
    try:
        page = requests.get('https://status.twitterstat.us/', timeout=5)
        soup = BeautifulSoup(page.content, 'html.parser')
        status = soup.find('span', class_='component-status').text.strip()
        return {'service': 'Twitter', 'status': status}
    except:
        return {'service': 'Twitter', 'status': 'Fehler'}

# Funktion: Slack-Status
def get_slack_status():
    try:
        page = requests.get('https://status.slack.com/', timeout=5)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Den Text des <h1> Tags abfragen, um den Status zu bekommen
        status_text = soup.find('h1', class_='text-center').text.strip()

        # Überprüfen, ob der Dienst läuft
        if 'up and running' in status_text.lower():
            return {'service': 'Slack', 'status': 'Operational'}
        else:
            return {'service': 'Slack', 'status': 'Degraded or Down'}

    except Exception as e:
        print(f"Fehler bei Slack: {e}")
        return {'service': 'Slack', 'status': 'Fehler'}

# Funktion: Spotify-Status
def get_spotify_status():
    try:
        page = requests.get('https://status.spotify.com/', timeout=5)
        soup = BeautifulSoup(page.content, 'html.parser')
        status = soup.find('span', class_='component-status').text.strip()
        return {'service': 'Spotify', 'status': status}
    except:
        return {'service': 'Spotify', 'status': 'Fehler'}

# Funktion: AWS-Status
def get_aws_status():
    try:
        page = requests.get('https://health.aws.amazon.com/govcloud/', timeout=5)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Überprüfen, ob der Dienst keine aktuellen Probleme hat
        status_text = soup.find('h2', class_='awsui_h2-variant_18wu0_1yxfb_176').text.strip()

        if 'No recent issues' in status_text:
            return {'service': 'AWS', 'status': 'Operational'}
        else:
            return {'service': 'AWS', 'status': 'Degraded or Down'}

    except Exception as e:
        print(f"Fehler bei AWS: {e}")
        return {'service': 'AWS', 'status': 'Fehler'}

@app.route('/')
def home():
    return "Status Monitor Backend - V1 läuft!"

# Haupt-Endpoint
@app.route('/status/all')
def get_all_statuses():
    statuses = [
        get_discord_status(),
        get_github_status(),
        get_zoom_status(),
        get_twitter_status(),
        get_slack_status(),
        get_spotify_status(),
        get_aws_status()
    ]
    return jsonify(statuses)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
