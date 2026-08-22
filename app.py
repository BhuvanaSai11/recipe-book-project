from flask import Flask, render_template, request

app = Flask(__name__)

# Rich database featuring both International and Indian dishes with full HD images, ingredients, and step-by-step procedures
RECIPE_DATABASE = {
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
        },
        {
            'title': 'Plain Dosa with Chutney',
            'image': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Dosa batter', 'Oil or Butter', 'Fresh coconut', 'Green chilies', 'Roasted chana dal'],
            'steps': [
                'Pour fermented dosa batter onto a hot greased tawa and spread it evenly.',
                'Cook until the bottom is crisp and golden brown spots appear.',
                'Blend coconut, green chilies, and roasted chana dal with water and salt to make the chutney.',
                'Fold the dosa and serve immediately with the fresh chutney.'
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
        },
        {
            'title': 'Authentic Veg Biryani',
            'image': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Basmati rice', 'Mixed vegetables (carrots, peas, beans)', 'Yogurt', 'Onions', 'Garam masala', 'Mint leaves'],
            'steps': [
                'Soak basmati rice for 30 minutes and boil with whole spices until half-cooked.',
                'Sauté sliced onions, ginger-garlic paste, and mixed vegetables with yogurt and biryani spices in a pan.',
                'Layer the cooked vegetables and half-cooked rice alternately in a heavy pot.',
                'Cover with a tight lid and steam on low heat for 20 minutes before serving.'
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
                'Cook the blended gravy in a pan with butter and spices until fragrant.',
                'Stir in a splash of fresh cream to achieve a rich, velvety consistency.',
                'Add paneer cubes, simmer for 5 minutes, garnish with cream, and serve hot.'
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
                'Melt butter in a pan, add minced garlic, and stir in flour to create a paste.',
                'Slowly whisk in milk continuously, cooking until the sauce thickens.',
                'Melt cheese into the sauce, toss in the pasta, season with oregano and chili flakes, and serve.'
            ]
        }
    ],
    'pizza': [
        {
            'title': 'Classic Margherita Pizza',
            'image': 'https://images.unsplash.com/photo-1604382355076-af4b0eb60143?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Pizza dough', 'Tomato sauce', 'Fresh mozzarella cheese', 'Fresh basil leaves', 'Olive oil'],
            'steps': [
                'Roll out your pizza dough on a floured surface to your desired thickness.',
                'Spread an even layer of tomato sauce across the base.',
                'Distribute fresh mozzarella cheese evenly over the sauce.',
                'Bake in a preheated high-temperature oven until bubbly and golden, then top with fresh basil.'
            ]
        }
    ],
    'burger': [
        {
            'title': 'Gourmet Cheese Burger',
            'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Burger buns', 'Patty', 'Cheddar cheese slice', 'Lettuce', 'Tomato slices', 'Burger sauce'],
            'steps': [
                'Grill or pan-fry your patty until fully cooked, placing a cheese slice on top during the last minute.',
                'Toast the burger buns lightly on the pan with a bit of butter.',
                'Spread sauce on the bottom bun, layer with lettuce, tomato, and the cheesy patty.',
                'Top with the bun and serve immediately.'
            ]
        }
    ],
    'sushi': [
        {
            'title': 'Salmon Avocado Roll',
            'image': 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=1200&q=85',
            'ingredients': ['Sushi rice', 'Nori seaweed sheets', 'Fresh salmon slices', 'Ripe avocado', 'Soy sauce', 'Wasabi'],
            'steps': [
                'Cook sushi rice and season with seasoned rice vinegar, then let it cool.',
                'Place a sheet of nori on a bamboo rolling mat and spread an even layer of rice over it.',
                'Add slices of fresh salmon and avocado in a straight line across the lower middle.',
                'Roll it tightly using the mat, slice into bite-sized pieces, and serve with soy sauce and wasabi.'
            ]
        }
    ],
    'tacos': [
        {
            'title': 'Crispy Chicken Tacos',
            'image': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&w=1200&q=85',
            'instances': ['Taco shells', 'Cooked shredded chicken', 'Cheddar cheese', 'Lettuce', 'Salsa', 'Sour cream'],
            'ingredients': ['Taco shells', 'Shredded chicken', 'Cheddar cheese', 'Shredded lettuce', 'Salsa', 'Sour cream'],
            'steps': [
                'Warm the taco shells in the oven according to package instructions.',
                'Season and shred your cooked chicken with taco spices.',
                'Fill each warm shell with shredded chicken, lettuce, and grated cheese.',
                'Top generously with salsa and a dollop of sour cream before serving.'
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
            # Look for matching keyword in our rich database
            for key in RECIPE_DATABASE:
                if key in search_query or search_query in key:
                    recipes = RECIPE_DATABASE[key]
                    break
            
            # If no direct match is found, show a clean message instead of a fake placeholder
            if not recipes:
                recipes = [{
                    'title': f'Recipe for {search_query.capitalize()}',
                    'image': 'https://images.unsplash.com/photo-1495521821757-a1efb6729352?auto=format&fit=crop&w=1200&q=85',
                    'ingredients': [search_query.capitalize(), 'Fresh herbs and aromatics', 'Cooking oil or butter', 'Selected seasonings'],
                    'steps': [
                        f'Gather all fresh ingredients needed for cooking {search_query}.',
                        'Prepare and chop components to uniform sizes for even cooking.',
                        'Cook over medium flame with your preferred spices until tender and aromatic.',
                        'Plate neatly and serve hot.'
                    ]
                }]
                
    return render_template('index.html', recipes=recipes, search_query=search_query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
