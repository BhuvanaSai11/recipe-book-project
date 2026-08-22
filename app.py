import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

SPOONACULAR_API_KEY = "c087b5e6e76c4afe9db832f136fcde57
"

# HD Image Database with International & Indian dishes + point-wise steps
RECIPE_DATABASE = {
    'dosa': [
        {
            'title': 'Crispy Masala Dosa',
            'image': 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Dosa batter', 'Boiled potatoes', 'Onions', 'Green chilies', 'Curry leaves', 'Mustard seeds', 'Turmeric', 'Ghee'],
            'steps': [
                'Boil and mash the potatoes, then sauté them with onions, green chilies, curry leaves, mustard seeds, and turmeric to make the filling.',
                'Heat a non-stick griddle (tawa) and pour a ladle of dosa batter in a circular motion to make a thin crepe.',
                'Drizzle ghee or oil around the edges and cook on medium-high heat until golden brown and crispy.',
                'Place the potato masala in the center, fold it over, and serve hot with coconut chutney and sambar.'
            ]
        },
        {
            'title': 'Plain Dosa with Chutney',
            'image': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Dosa batter', 'Oil or Butter', 'Coconut', 'Green chilies', 'Roasted chana dal'],
            'steps': [
                'Pour fermented dosa batter onto a hot greased tawa and spread it evenly.',
                'Cook until the bottom is crisp and golden brown spots appear.',
                'Blend fresh coconut, green chilies, and roasted chana dal with water and salt to make the chutney, then temper with mustard seeds.',
                'Fold the dosa and serve immediately with the fresh chutney.'
            ]
        }
    ],
    'biryani': [
        {
            'title': 'Hyderabadi Chicken Dum Biryani',
            'image': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Basmati rice', 'Chicken', 'Yogurt', 'Fried onions', 'Ginger-garlic paste', 'Biryani masala', 'Saffron milk', 'Mint and coriander'],
            'steps': [
                'Marinate chicken with yogurt, fried onions, ginger-garlic paste, spices, mint, and lemon juice for at least 2 hours.',
                'Boil soaked basmati rice with whole spices until it is 70% cooked (semi-cooked).',
                'Layer the partially cooked rice over the raw marinated chicken in a heavy-bottomed pot.',
                'Top with saffron milk, ghee, and fried onions, seal tightly with dough or foil, and cook on low heat (dum) for 45 minutes.'
            ]
        }
    ],
    'paneer': [
        {
            'title': 'Paneer Butter Masala',
            'image': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Paneer cubes', 'Tomatoes', 'Onions', 'Cashews', 'Butter', 'Fresh cream', 'Garlic and ginger', 'Garam masala'],
            'steps': [
                'Sauté tomatoes, onions, ginger, garlic, and cashews in butter until soft, then blend into a smooth puree.',
                'Cook the blended gravy in a pan with butter, chili powder, and garam masala until fragrant.',
                'Stir in a splash of water and fresh cream to achieve a rich, velvety consistency.',
                'Add paneer cubes, simmer for 5 minutes, garnish with a swirl of cream, and serve hot.'
            ]
        }
    ],
    'pasta': [
        {
            'title': 'Creamy White Sauce Pasta',
            'image': 'https://images.unsplash.com/photo-1621996346565-e3d5d6281297?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Penne pasta', 'Butter', 'All-purpose flour', 'Milk', 'Garlic', 'Mozzarella cheese', 'Oregano', 'Chili flakes'],
            'steps': [
                'Boil penne pasta in salted water until al dente, then drain.',
                'Melt butter in a pan, add minced garlic, and stir in flour to create a paste (roux).',
                'Slowly whisk in milk continuously to avoid lumps, cooking until the sauce thickens.',
                'Melt cheese into the sauce, toss in the boiled pasta, season with oregano and chili flakes, and serve hot.'
            ]
        }
    ],
    'pizza': [
        {
            'title': 'Classic Margherita Pizza',
            'image': 'https://images.unsplash.com/photo-1604382355076-af4b0eb60143?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Pizza dough', 'San Marzano tomato sauce', 'Fresh mozzarella cheese', 'Fresh basil leaves', 'Olive oil'],
            'steps': [
                'Roll out your pizza dough on a floured surface to your desired thickness.',
                'Spread an even layer of tomato sauce across the base, leaving a small border for the crust.',
                'Tear fresh mozzarella cheese and distribute it evenly over the sauce.',
                'Bake in a preheated high-temperature oven until the crust is golden and cheese is bubbly, then top with fresh basil.'
            ]
        }
    ],
    'burger': [
        {
            'title': 'Gourmet Cheese Burger',
            'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Burger buns', 'Ground beef or veg patty', 'Cheddar cheese slice', 'Lettuce', 'Tomato slices', 'Burger sauce'],
            'steps': [
                'Grill or pan-fry your patty until fully cooked and juicy, placing a cheese slice on top during the last minute to melt.',
                'Toast the burger buns lightly on the pan with a bit of butter.',
                'Spread sauce on the bottom bun, layer with fresh lettuce, tomato, the cheesy patty, and top bun.',
                'Serve immediately with fries.'
            ]
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
            for key in RECIPE_DATABASE:
                if key in search_query:
                    recipes = RECIPE_DATABASE[key]
                    break
            
            # API fallback with HD image formatting
            if not recipes:
                url = f'https://api.spoonacular.com/recipes/complexSearch?query={search_query}&number=12&apiKey={SPOONACULAR_API_KEY}'
                try:
                    response = requests.get(url, timeout=5)
                    data = response.json()
                    if response.status_code == 200 and 'results' in data:
                        for item in data['results']:
                            recipes.append({
                                'title': item['title'],
                                'image': item['image'],
                                'ingredients': ['Main components sourced via global recipe catalog.'],
                                'steps': [
                                    'Prepare your core ingredients.',
                                    'Cook over medium heat with appropriate seasoning until done.',
                                    'Plate up and serve hot.'
                                ]
                            })
                except Exception as e:
                    print(f"API error: {e}")
            
            if not recipes:
                recipes = [{
                    'title': f'Delicious Homemade {search_query.capitalize()}',
                    'image': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=1200&q=85',
                    'ingredients': [search_query.capitalize(), 'Essential spices', 'Fresh oil or butter'],
                    'steps': [
                        f'Clean and prep your primary ingredient: {search_query}.',
                        'Heat oil in a pan, add aromatics, and sauté thoroughly.',
                        'Simmer with seasonings until cooked to perfection and serve.'
                    ]
                }]
                
    return render_template('index.html', recipes=recipes, search_query=search_query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
