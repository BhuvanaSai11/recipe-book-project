from flask import Flask, render_template, request

app = Flask(__name__)

RECIPE_DATABASE = {
    'banana cake': [
        {
            'title': 'Eggless Whole Wheat Banana Cake',
            'image': 'https://images.unsplash.com/photo-1603532648955-039310d9ed75?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Ripe bananas', 'Whole wheat flour', 'Jaggery or sugar', 'Milk or curd', 'Baking powder', 'Baking soda', 'Vanilla extract', 'Butter or oil'],
            'steps': [
                'Mash the ripe bananas thoroughly in a bowl until smooth.',
                'Mix in the melted butter/oil, sugar/jaggery, and vanilla extract until well combined.',
                'Sift in the whole wheat flour, baking powder, and baking soda, gently folding it together while adding milk or curd to get a smooth batter.',
                'Pour into a greased baking pan and bake in your air fryer or oven at 180°C for 25-30 minutes until a toothpick inserted comes out clean.'
            ]
        }
    ],
    'donuts': [
        {
            'title': 'Air Fryer Homemade Donuts',
            'image': 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['All-purpose flour', 'Warm milk', 'Sugar', 'Yeast or baking powder', 'Butter', 'Vanilla', 'Glaze (sugar and milk)'],
            'steps': [
                'Mix warm milk, sugar, and yeast/baking powder, then combine with flour and melted butter to knead into a soft dough.',
                'Let the dough rise, then roll it out and cut into donut shapes using a cutter or glass.',
                'Lightly brush the donuts with oil or butter and place them in your air fryer.',
                'Air fry at 180°C for 6-8 minutes until golden, then dip them in a sweet milk glaze.'
            ]
        }
    ],
    'puffs': [
        {
            'title': 'Crispy Egg Puffs',
            'image': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Puff pastry sheets or rough puff dough', 'Boiled eggs', 'Onions', 'Green chilies', 'Turmeric powder', 'Red chili powder', 'Garam masala'],
            'steps': [
                'Finely chop onions and sauté them in a pan with green chilies and dry spices until soft and golden.',
                'Cut your boiled eggs in half lengthwise.',
                'Roll out your pastry dough into squares, place a spoonful of onion masala and a half-egg in the center.',
                'Seal the edges tightly and air bake until golden and flaky.'
            ]
        }
    ],
    'dosa': [
        {
            'title': 'Crispy Masala Dosa',
            'image': 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Dosa batter', 'Boiled potatoes', 'Onions', 'Green chilies', 'Curry leaves', 'Mustard seeds', 'Turmeric', 'Ghee'],
            'steps': [
                'Boil and mash the potatoes, then sauté them with onions, green chilies, curry leaves, mustard seeds, and turmeric.',
                'Heat a non-stick griddle (tawa) and pour a ladle of dosa batter in a circular motion to make a thin crepe.',
                'Drizzle ghee around the edges and cook on medium-high heat until golden brown and crispy.',
                'Place the potato masala in the center, fold it over, and serve hot with chutney and sambar.'
            ]
        }
    ],
    'biryani': [
        {
            'title': 'Hyderabadi Chicken Dum Biryani',
            'image': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Basmati rice', 'Chicken', 'Yogurt', 'Fried onions', 'Ginger-garlic paste', 'Biryani masala', 'Saffron milk', 'Mint'],
            'steps': [
                'Marinate chicken with yogurt, fried onions, ginger-garlic paste, spices, and mint for at least 2 hours.',
                'Boil soaked basmati rice with whole spices until 70% cooked.',
                'Layer the partially cooked rice over the raw marinated chicken in a heavy pot.',
                'Top with saffron milk and ghee, seal tightly, and cook on low heat (dum) for 45 minutes.'
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
                if key in search_query or search_query in key:
                    recipes = RECIPE_DATABASE[key]
                    break
            
            if not recipes:
                recipes = [{
                    'title': f'Recipe for {search_query.capitalize()}',
                    'image': 'https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=1200&q=85',
                    'ingredients': ['Main ingredients for ' + search_query, 'Required spices or seasonings', 'Cooking oil or butter'],
                    'steps': [
                        f'Prepare all components required for {search_query}.',
                        'Cook or bake using standard proportions until done.',
                        'Serve hot and enjoy!'
                    ]
                }]
                
    return render_template('index.html', recipes=recipes, search_query=search_query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
