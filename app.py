from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    recipes = []
    search_query = ''
    
    if request.method == 'POST':
        search_query = request.form.get('ingredient', '').strip().lower()
        if search_query:
            dish_name = search_query.title()
            
            # This dynamically creates a custom card for whatever you type
            recipes = [{
                'title': f'{dish_name} Special Recipe',
                'image': f'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=1200&q=85',
                'ingredients': [
                    f'Main ingredient: {dish_name}',
                    'Fresh onions, ginger, and garlic paste',
                    'Cooking oil or butter',
                    'Signature spices, salt, and pepper to taste'
                ],
                'steps': [
                    f'Clean and prep your ingredients for {dish_name}.',
                    'Heat oil in a pan, add aromatics, and sauté until golden brown.',
                    'Add your main component and spices, cooking thoroughly on medium heat.',
                    'Garnish, plate hot, and serve immediately.'
                ]
            }]
                
    return render_template('index.html', recipes=recipes, search_query=search_query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
