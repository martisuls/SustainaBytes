# save the programm steps in functions 
# first, programm a function to get an user input with streamlit of the available groceries 
# second, programm a function to get an user input with streamlit of the food preferences 
# (the food and preferences data will then be used for the API call that gets the recipe)

#Marti, Mariam, David, (Sibelly) 
#import libraries
import streamlit as st
import requests
#this library was imported to be able to read Nutrients which were displayed in Json format
from bs4 import BeautifulSoup

#Spoonacular API key, needed to access API
API_KEY = "5397833665e64aaf9e8e2bcc02471f85"

def search_by_ingredients(ingredients):
    url = f'https://api.spoonacular.com/recipes/findByIngredients'
    params = {
        'apiKey': API_KEY,
        'number': 15,  # Number of recipes to fetch
        'ingredients': ingredients,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Failed to fetch recipes by ingredients. Please try again later.")
        return []


# Getting recipe details (meaning how to cook the recipe) by recipe ID. An ID is used, as Spoonacular API has an ID for each of their recipes
def fetch_recipe_details(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch recipe details.")

# Getting nutrition (such as calories) information for a recipe by recipe ID
def fetch_nutrition_info(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json?apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch nutrition information.")

# Website Title
st.title("Sustainabytes")

# Input field for ingredients
ingredients_input = st.text_area('Enter ingredients:')

# Multiselect for cuisine
cuisine_options = ['African', 'American', 'Cajun', 'Caribbean', 'Chinese', 'Eastern European', 'European', 'French', 'German', 'Greek', 'Indian', 'Italian', 'Japanese', 'Korean', 'Latin American', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Nordic', 'Spanish', 'Thai', 'Vietnamese']
selected_cuisine = st.multiselect('Select Cuisine:', ["All Cuisines"] + cuisine_options)
# code to select all cuisine types when selecitng "All Cuisines"
if "All Cuisines" in selected_cuisine:
    selected_cuisine=cuisine_options

# Multiselect for intolerance and putting all at the end
intolerance_options = ['Dairy', 'Egg', 'Gluten', 'Grain', 'Peanut', 'Seafood', 'Sesame', 'Shellfish', 'Soy',]
selected_intolerance = st.multiselect('Select Intolerance:', intolerance_options + ["All Intolerances"])
# same code as above to select all intolerances
if "All Intolerances" in intolerance_options:
    selected_intolerance=intolerance_options

# Multiselect for diet
diet_options = ['Gluten Free', 'Ketogenic', 'Vegetarian', 'Lacto-Vegetarian', 'Vegan', 'Pescetarian']
selected_diet = st.multiselect('Select Diet:', diet_options)

if st.button('Search Recipes by Ingredients'):
    recipes = search_by_ingredients(ingredients_input)

    # Display fetched recipes
    if recipes:
        st.subheader("Here are some recipe suggestions:")
        for recipe in recipes:
            st.write(f"- {recipe['title']}")
            # Fetching and displaying recipe details
            details = fetch_recipe_details(recipe['id'])
            if details:
                st.write("Recipe Details:")
                st.write(f"Instructions: {details['instructions']}")
                st.write(f"Servings: {details['servings']}")
                #getting nutrient info
                nutrients = fetch_nutrition_info(recipe['id'])
                if nutrients:
                    st.write("Nutritional Information:")
                    for nutrient in nutrients['nutrients']:
                        st.write(f"{nutrient['name']}: {nutrient['amount']} {nutrient['unit']}")
                            
    else:
        st.write("No recipes found. Try adjusting your search criteria.")