import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Get a free key at https://spoonacular.com/food-api/console#Dashboard
# On Render: Dashboard -> your service -> Environment -> add SPOONACULAR_API_KEY
API_KEY = os.environ.get("c087b5e6e76c4afe9db832f136fcde57
")
BASE_URL = "https://api.spoonacular.com/recipes"


def search_recipes(query, number=3):
    """Search Spoonacular for recipes matching the query, with full info."""
    url = f"{BASE_URL}/complexSearch"
    params = {
        "apiKey": API_KEY,
        "query": query,
        "number": number,
        "addRecipeInformation": True,  # gives us ingredients + instructions directly
        "fillIngredients": True,
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])


def format_recipe(item):
    """Turn one Spoonacular result into the shape our template expects."""
    ingredients = [
        ing.get("original", ing.get("name", ""))
        for ing in item.get("extendedIngredients", [])
    ] or ["Ingredient list not available for this recipe."]

    steps = []
    instructions = item.get("analyzedInstructions", [])
    if instructions and instructions[0].get("steps"):
        steps = [s["step"] for s in instructions[0]["steps"]]
    else:
        # Some recipes only have a plain-text instructions blob
        raw = item.get("instructions")
        steps = [raw] if raw else ["No step-by-step instructions available."]

    return {
        "title": item.get("title", "Untitled Recipe"),
        "image": item.get("image") or "https://via.placeholder.com/400x300?text=No+Image",
        "ingredients": ingredients,
        "steps": steps,
    }


@app.route("/", methods=["GET", "POST"])
def home():
    recipes = []
    search_query = ""
    error = None

    if request.method == "POST":
        search_query = request.form.get("ingredient", "").strip()

        if not API_KEY:
            error = "Server is missing SPOONACULAR_API_KEY — set it in your environment."
        elif search_query:
            try:
                results = search_recipes(search_query)
                if results:
                    recipes = [format_recipe(item) for item in results]
                else:
                    error = f"No recipes found for '{search_query}'. Try a different search."
            except requests.exceptions.RequestException as e:
                error = f"Couldn't reach the recipe API right now: {e}"

    return render_template(
        "index.html",
        recipes=recipes,
        search_query=search_query,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)
