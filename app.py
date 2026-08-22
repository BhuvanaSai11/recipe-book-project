import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

SPOONACULAR_API_KEY = "c087b5e6e76c4afe9db832f136fcde57"

INDIAN_DISHES = {
    'dosa': [
        {
            'title': 'Crispy Masala Dosa',
            'image': 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=600&q=80'
        },
        {
            'title': 'Plain Dosa with Chutney',
            'image': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=600&q=80'
        }
    ],
    'biryani': [
        {
            'title': 'Hyderabadi Chicken Dum Biryani',
            'image': 'https://www.themealdb.com/images/media/meals/xrwwuw1503562699.jpg'
        }
    ],
    'paneer': [
        {
            'title': 'Paneer Butter Masala',
            'image': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=600&q=80'
        }
    ]
}

@app.route('/', methods=['GET', 'POST'])
def home():
    recipes = []
    search_query = ''
    
    if request.method == 'POST':
        search_query = request.form.get('ingredient', '').strip().lower()
        if search_query:
            for key in INDIAN_DISHES:
                if key in search_query:
                    recipes = INDIAN_DISHES[key]
                    break
            
            if not recipes:
                url = f'https://api.spoonacular.com/recipes/complexSearch?query={search_query}&number=12&apiKey={SPOONACULAR_API_KEY}'
                try:
                    response = requests.get(url, timeout=5)
                    data = response.json()
                    if response.status_code == 200 and 'results' in data:
                        recipes = data['results']
                except Exception as e:
                    print(f"API error: {e}")
            
            if not recipes:
                recipes = [{
                    'title': f'Delicious {search_query.capitalize()}',
                    'image': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80'
                }]
                
    return render_template('index.html', recipes=recipes, search_query=search_query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
