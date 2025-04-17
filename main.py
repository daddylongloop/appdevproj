from typing import Final, Tuple
import pandas as pd 
pd.options.display.max_colwidth = 1000 # so the data doesnt get cut off in print statements

# useless columns 
RAWRecipes = pd.read_csv("./RAW_recipes.csv")
RAWRecipes = RAWRecipes.drop('n_steps', axis=1) 
# RAWRecipes = RAWRecipes.drop('tags', axis=1) 
RAWRecipes = RAWRecipes.drop('contributor_id', axis=1) 
RAWRecipes = RAWRecipes.drop('n_ingredients', axis=1) 
RAWRecipes = RAWRecipes.drop('submitted', axis=1) 
label: Final = 0
data: Final = 1

import mysql.connector
cursor = (cnx := mysql.connector.connect(
          host="127.0.0.1", user="", password="", get_warnings=True
)).cursor()


add_recipe = ("INSERT INTO Recipes "
         "(NID,     name,    id,      minutes,    nutrition,     steps,      description) "
"VALUES (%(NID)s, %(name)s, %(id)s, %(minutes)s, %(nutrition)s, %(steps)s, %(description)s)")

add_tag_asgn = ("INSERT INTO TagsASGN "
                "        (ID,      recipeID,     tagID) "
                "VALUES (%(ID)s, %(recipeID)s, %(tagID)s)")

add_ingredient = ("INSERT INTO Ingredients "
                "         (ID,      name) "
                "VALUES (%(ID)s, %(name)s)")

add_ingredient_asgn = ("INSERT INTO IngredientsASGN "
                "        (ID,      recipeID,     ingredientID) "
                "VALUES (%(ID)s, %(recipeID)s, %(ingredientID)s)")

c_row = (list(RAWRecipes.iterrows()))

recipe = {'NID': None} # for uplaoding a recipe to recipes table
assgn_ingredient = {'ID': None} # for linking recipes to ingredients

important_tags = ["vegan", "vegetarian", "gluten-free", "dairy-free", 
                  "nut-free", "egg-free", "low-carb", 
                  "low-fat", "high-protein", "sugar-free",
                  "side-dishes", "main-dishes", "desserts"]

def parse_columns(row):
    for c in row.splitlines(): # iterate over each column
        column = list(c.partition(' ')[::2]) # split into label and value
        column[data] = column[data].strip() # remove whitespace 
        yield column

def parse_ingredients(ingredients_entry):
    try: 
        ingredients = eval(ingredients_entry)
    except Exception as e: return []

    for ing in ingredients:
            yield ing
    
def parse_tags(tags_entry):
    ret = []
    try: tags = eval(tags_entry)
    except Exception as e: return []
    for tag in tags:
        if tag in important_tags:
            ret.append(tag)
    return ret

def extract_data(index_of_row) -> Tuple[dict, list]:
    temp_recipe = {}
    ingredients = []

    for column in parse_columns(c_row[index_of_row][1].to_string()):

        if not column[label] == 'ingredients':
            temp_recipe[column[label]] = column[data]

        if column[label] == 'ingredients':
            ingredients = list(parse_ingredients(column[data]))
        
        if column[label] == 'tags':
            tags = parse_tags(column[data])

    return (temp_recipe, ingredients, tags)

def sql_search_ingredient(_cursor, ingredient_name):
    search_query = "SELECT * FROM Ingredients WHERE name = %(name)s"
    _cursor.execute(search_query, {'name': ingredient_name})
    result = _cursor.fetchone()  # Fetch one result (or use fetchall() for multiple results)
    return result is not None  # Return True if the ingredient exists, False otherwise

for i in range(1,2): # can do in chunks of 33,473 ( will run 8 times ) ?
    recipe, ingredients, tags = extract_data(i)
    last_ingredient_id = None
    for ing in ingredients:    
        # TODO look if there is an ingredient with the name, if not then add it to the table
        if sql_search_ingredient(cursor, ing) == False:
            ingredient = {"ID": None, "name": ing}
            cursor.execute(add_ingredient, ingredient)
            cursor.execute("SELECT LAST_INSERT_ID()")
            last_ingredient_id = cursor.fetchone()[0]  # Fetch the first column of the result

    # TODO then uplaod recipe to the recipe table
    recipe['NID'] = None
    cursor.execute(add_recipe, recipe)
    # cursor.execute("SELECT LAST_INSERT_ID()")
    # last_recipe_NID = cursor.fetchone()[0]
    # TODO link tags
    #  tags.indexof(tag) + 1 ? 
    # TODO then uplaod asgn to the ingredientASGN table
    
    # assgn_ingredient['recipeID'] = last recipe NID

    # assgn_ingredient['ingredientID'] = last ingredinet ID
    # assgn_ingredient['ID'] = None
    # cursor.execute(add_ingredient_asgn, assgn_ingredient)

cnx.close()