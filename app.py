from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', '')
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def home():
    return jsonify({
        'message': 'Weather API Service',
        'endpoints': {
            '/weather?city=<city_name>': 'Get weather by city name',
            '/health': 'Health check'
        },
        'version': '2.0.0',
        'status': 'running'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    
    try:
        response = requests.get(WEATHER_API_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            weather_info = {
                'city': city,
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'timestamp': datetime.now().isoformat(),
                'version': '2.0.0',
                'new_feature': 'Weather forecast updated!'
                
            }
            return jsonify(weather_info)
        else:
            return jsonify({'error': data.get('message', 'City not found')}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)