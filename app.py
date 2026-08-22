import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Replace with your actual Spoonacular API key
SPOONACULAR_API_KEY = "paste_your_real_key_here"

@app.route('/', methods=['GET', 'POST'])
def home():
  recipes = []
  search_query = ''

  if request.method == 'POST':
    search_query = request.form.get('ingredient', '').strip().lower()
    if search_query:
      url = f'https://api.spoonacular.com/recipes/complexSearch?query={search_query}&number=12&apiKey={SPOONACULAR_API_KEY}'
      try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data and 'results' in data:
          recipes = data['results']
      except Exception as e:
        print(f'Error fetching recipes: {e}')

  return render_template(
      'index.html', recipes=recipes, search_query=search_query
  )


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
