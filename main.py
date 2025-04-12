from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

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

@app.route('/')
def home():
    return "Status Monitor Backend - V1 läuft!"

# Haupt-Endpoint
@app.route('/status/all')
def get_all_statuses():
    statuses = [
        get_discord_status(),
        get_github_status(),
        get_zoom_status()
    ]
    return jsonify(statuses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
