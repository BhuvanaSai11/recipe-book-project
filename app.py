import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# ============================================================
# IMPORTANT: DO NOT put your actual API key on the line below.
# Leave it exactly as "SPOONACULAR_API_KEY" (a string literal).
# Your real key goes ONLY in Render's dashboard:
#   Render -> your service -> Environment -> Add Environment Variable
#   Key:   SPOONACULAR_API_KEY
#   Value: <your actual key, e.g. c087b5e6e76c4afe9db832f136fcde57>
# This line just reads whatever value Render has stored there.
# ============================================================
API_KEY = os.environ.get("SPOONACULAR_API_KEY")

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
            # This means Render's Environment tab is missing SPOONACULAR_API_KEY,
            # or it hasn't redeployed since you added it.
            error = "Server is missing SPOONACULAR_API_KEY — set it in Render's Environment tab."
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
