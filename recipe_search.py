import pickle
import pandas as pd
import csv
import json
from AllRecipesScrape import *
from tfmodel import *
from main import *



def capitalize(str):
    temp_list = str.split()
    for i, j in enumerate(temp_list):
        temp_list[i] = j.capitalize()


    separator = ' '
    return separator.join(temp_list)

def find_food_num(food):
    """
    (str) -> int
    Finds the id number of a specific ingrediant
    """
    infile = open("Database//Ingrediants.pkl",'rb')
    new_dict = pickle.load(infile)
    infile.close()

    series1 = new_dict["raw_ingr"]
    series1 = pd.Series(dict((v,k) for k,v in series1.iteritems()))
    series2 = new_dict["id"]
    value = series1[food]
    id_num = series2[value]
    return str(id_num)

def find_food_name(food_id):
    """
    (int) -> str
    Finds the food name of a specific ingrediant
    """
    infile = open("Database//Ingrediants.pkl",'rb')
    new_dict = pickle.load(infile)
    infile.close()

    series1 = new_dict["id"]
    series1 = pd.Series(dict((v,k) for k,v in series1.iteritems()))
    series2 = new_dict["raw_ingr"]
    value = series1[food_id]
    return series2[value]



def get_ingr(ingr_list):
    """
    (list) -> list
    Returns a list of ingrediant names using the ingrediant id numbers
    """
    ingr_name = []
    for id_num in ingr_list:
        ingr_name.append(find_food_name(int(id_num)))

    return ingr_name


def get_recipe(recipe_id):
    """
    (int) -> dict
    Returns a dictionary with all the needed information using the recipe id
    """
    recipe = {}
    with open("Database//RAW_recipes.csv", encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == recipe_id:
                recipe["Name"] = capitalize(row[0])
                recipe["Minutes"] = row[2]
                recipe["Nutrition"] = row[6].strip('][').split(', ')
                recipe["Steps"] = row[8].strip('][').split(', ')
                recipe["Description"] = row[9]

    return recipe



def find_recipe(foods):
    """
    (list) -> dict
    Finds the recipe and returns a dictionary with all the needed information
    """
    id_list = []
    recipe_list = []
    recipe = {}
    for a in foods:
        id_num = find_food_num(a)
        id_list.append(id_num)


    with open("Database//PP_recipes.csv") as file:
        reader = csv.reader(file)

        count = 0
        for row in reader:

            if count < 6:
                ingr_list = row[-1].strip('][').split(', ')
                check = all(item in ingr_list for item in id_list)
                if check is True:
                    count += 1
                    recipe = get_recipe(row[0])
                    recipe["Ingrediants"] = get_ingr(ingr_list)
                    recipe["Image"] = getImage(recipe["Name"])
                    recipe_list.append(recipe)

            else:
                break


        temp_dict = {'Detected Foods': [i for i in foods]}
        recipe_list.append(temp_dict)

        return recipe_list



if __name__ == "__main__":
    foods = ["banana", "apple"]
    a = find_recipe(foods)
    with open("output", "w") as f:
        json.dump(a, f)
