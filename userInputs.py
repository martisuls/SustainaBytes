#Marti, Sibelly

# --- Import libraries ---
import streamlit as st
import apiCall
import matplotlib.pyplot as plt

# --- Function to check if recipe matches the user's dietary preferences ---
def recipe_matches_preferences(diet_options:list, recipe_details):
    if recipe_details:
        # Check if a preference was selected
        if 'Vegetarian' in diet_options: 
            if recipe_details["vegetarian"] == False: # We serach in all recipes if they are vegeterian. If not (False), then we skip the recipe 
                return False
        if 'Vegan' in diet_options:
            if recipe_details["vegan"] == False: # Check if recipe is vegan
                return False
        if 'Dairy Intolerance' in diet_options:
            if recipe_details["dairyFree"] == False: # Check if recipe is dairy-free
                return False
        if 'Gluten Free' in diet_options:
            if recipe_details["glutenFree"] == False: # Check if recipe is gluten-free
                return False
    
    if len(diet_options) == 0 or 'None' in diet_options: # If no preference is selected the programm continues to run
       return True

    return True


#--- Website App Title & Description ---
st.set_page_config(page_title="SustainaBytes", page_icon="🥗") # Set page title and icon
st.title("SustainaBytes") # Displaying the title
st.write("Find delicious recipes with the ingredients you have at home and help reduce food waste!") # Displaying description


# --- User inputs ---
# Input field for ingredients
ingredients_options = ingredients = ['Chicken', 'Tomato', 'Onion', 'Potato', 'Pasta','Pepper', 'Eggs', 'Milk', 'Rice','Cream cheese', 'Carrots']
selected_ingredients = st.multiselect('Select Ingredients:', ingredients_options)

# Multiselect for cuisine
cuisine_options = ['African', 'American', 'Cajun', 'Caribbean', 'Chinese', 'Eastern European', 'European', 'French', 'German', 'Greek', 'Indian', 'Italian', 'Japanese', 'Korean', 'Latin American', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Nordic', 'Spanish', 'Thai', 'Vietnamese']
selected_cuisine = st.multiselect('Select Cuisine:', cuisine_options)

# Multiselect for diet preferences
diet_options = ['Vegetarian','Vegan', 'Dairy Intolerance', 'Gluten Free']
selected_diet = st.multiselect('Diet preferences:', diet_options)


# --- Fetch & Display Recipes ---
if st.button(' 🔍 Find Recipes'):
    # Fetch recipes based on selected ingredients and cuisine
    recipes = apiCall.search_by_ingredients_cuisine(selected_ingredients, selected_cuisine) 

    if recipes:
        # Displaying subheader for recipe suggestions
        st.subheader("Here are some recipe suggestions:") 

        for recipe in recipes["results"]:
            #Fetch details of each recipe
            details = apiCall.fetch_recipe_details(recipe["id"])

            # Checking if the recipe matches dietary preferences with the function above
            if recipe_matches_preferences(selected_diet, details):  
                recipe_name = recipe['title']
                recipe_id = recipe['id']
                
                #Display recipe name in a larger font size & image
                st.write(f"### {recipe_name}")
                st.image(recipe['image'])
                
                #Display details
                if details:
                    st.write(f"Servings: {details['servings']}")
                    st.write("Recipe Instructions:")
                    st.write(details['instructions'])
    
                #Display nutrient information
                nutrients = apiCall.fetch_nutrition_info(recipe['id']) # Fetch nutrient information
                if nutrients:
                    # Extract nutrient names and values for the pie chart
                    nutrient_names = [nutrient['name'] for nutrient in nutrients['nutrients']]
                    nutrient_values = [nutrient['amount'] for nutrient in nutrients['nutrients']]

                    # Display pie chart of nutrients
                    st.write("Pie Chart of Nutrients:")
                    fig, ax = plt.subplots()
                    ax.pie(nutrient_values[:3], labels=nutrient_names[:3], autopct='%1.1f%%') # Only taking the top 3 nutrients (can be adjusted)
                    st.pyplot(fig) #Display 

    else:
        st.write("No recipes found. Try adjusting your search criteria.")