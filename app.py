from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    recipes = []
    search_query = ''
    
    if request.method == 'POST':
        search_query = request.form.get('ingredient', '').strip().lower()
        if search_query:
            url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={search_query}"
            try:
                response = requests.get(url, timeout=5)
                data = response.json()
                if data and data.get('meals'):
                    recipes = data['meals']
            except Exception as e:
                print(f"Error fetching recipes: {e}")

    return render_template('index.html', recipes=recipes, search_query=search_query)

@app.route('/recipe/<meal_id>')
def recipe_detail(meal_id):
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    recipe = None
    ingredients = []
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data and data.get('meals'):
            meal = data['meals'][0]
            recipe = meal
            
            # Extract ingredients and measurements
            for i in range(1, 21):
                ingredient = meal.get(f'strIngredient{i}')
                measure = meal.get(f'strMeasure{i}')
                if ingredient and ingredient.strip():
                    ingredients.append(f"{measure.strip() if measure else ''} {ingredient.strip()}".strip())
    except Exception as e:
        print(f"Error fetching detail: {e}")

    return render_template('detail.html', recipe=recipe, ingredients=ingredients)

if __name__ == '__main__':
    app.run(debug=True)