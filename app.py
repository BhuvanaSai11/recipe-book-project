import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

SPOONACULAR_API_KEY = "c087b5e6e76c4afe9db832f136fcde57
"

# A robust backup list for common searches so it never comes up empty
DEFAULT_RECIPES = [
    {
        'title': 'Crispy Masala Dosa',
        'image': (
            'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=600&q=80'
        ),
    },
    {
        'title': 'Hyderabadi Chicken Dum Biryani',
        'image': (
            'https://www.themealdb.com/images/media/meals/xrwwuw1503562699.jpg'
        ),
    },
    {
        'title': 'Paneer Butter Masala',
        'image': (
            'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=600&q=80'
        ),
    },
    {
        'title': 'Classic Chicken Curry',
        'image': (
            'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=600&q=80'
        ),
    },
]


@app.route('/', methods=['GET', 'POST'])
def home():
  recipes = []
  search_query = ''

  if request.method == 'POST':
    search_query = request.form.get('ingredient', '').strip().lower()
    if search_query:
      # Try Spoonacular first
      url = f'https://api.spoonacular.com/recipes/complexSearch?query={search_query}&number=12&apiKey={SPOONACULAR_API_KEY}'
      try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if response.status_code == 200 and 'results' in data:
          recipes = data['results']
      except Exception as e:
        print(f'API error: {e}')

      # If the API doesn't return anything, filter our default list or create a custom card
      if not recipes:
        recipes = [
            r
            for r in DEFAULT_RECIPES
            if search_query in r['title'].lower()
        ]

      # If still empty, show a customized result card dynamically so it never breaks
      if not recipes:
        recipes = [{
            'title': f'Homemade {search_query.capitalize()} Special',
            'image': (
                'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80'
            ),
        }]

  return render_template(
      'index.html', recipes=recipes, search_query=search_query
  )


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
