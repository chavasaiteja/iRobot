import sys
import requests
import pickle
#nltk is natural lanuage processing tool kit that has libraries for various NLP algorithms
from nltk import pos_tag,word_tokenize
from nltk.stem import PorterStemmer
import time

#Porter stemming alogrithm is used to covert all the tokens to thier root words
ps = PorterStemmer()

#api-endpoint
URL_Search = "http://food2fork.com/api/search"
URL_Recipe = "http://food2fork.com/api/get"

#Key
KEY = "08b069a3f7a8d15acc807d6b637b8dc1"

list_of_ingredients = []

def iBotIntro():
    print("Hello....I am Ibot")
    time.sleep(2)
    print("I am here to get you the best recipe you can prepare with the ingredients you have :-)")
    time.sleep(2)
    print("Let's get started!!!!!!!")
    time.sleep(2)
    print("Tell me what all ingredients you have\n")
    time.sleep(2)

def get_input():
    #Get the number of ingredients from the user and validate if no of ingredients is integer
    while True:
        try:
            no_of_ingredients = int(input("Enter the no of ingredients: "))
            if no_of_ingredients<1:
                print("Sorry, input must be a positive integer, try again")
                continue
        except ValueError:
            print("Please Enter a Valid Integer")
            continue
        else:
            break
    query = ""
    #Assuming ingredients as strings
    for i in range(0,int(no_of_ingredients)):
        ingredient=input("Enter ingredient no " + str(i + 1) + " : ")
        list_of_ingredients.append(ps.stem(ingredient))
        query = query+ingredient
        if i != int(no_of_ingredients)-1:
            query=query+","

    print("\nThe entered ingredients are as follows :")
    print(str(list_of_ingredients))
    return query

def get_Recipe(query):
    PARAMS = {'key': KEY, 'q': query, 'sort':'social_rank'}
    data = requests.get(url = URL_Search,params = PARAMS)
    json_data=data.json()
    no_of_recipes=json_data['count']
    recipe_id=None
    if no_of_recipes > 1:
        recipe_id=json_data['recipes'][0]['recipe_id']
        recipe_title=json_data['recipes'][0]['title']
        print("Here you go, the most Trending Recipe you can prepare with your ingredients")
        print("\nRecipe : {} ".format(recipe_title))
    return recipe_id


def get_Recipe_ingredients(recipe_id):
    listed_ingredients = set(list_of_ingredients)
    prefered_ingredients = set()
    missing_temp_ingredients = set()
    recipe_PARAMS = {'key': KEY, 'rId': recipe_id}
    recipe_data = requests.get(url=URL_Recipe, params=recipe_PARAMS)
    json_recipe_data=recipe_data.json()
    ingredientsLists=json_recipe_data['recipe']['ingredients']
    for ingredient in ingredientsLists:
        pos_tags = pos_tag(word_tokenize(ingredient))
        for tag in pos_tags:
            if tag[1].startswith('NN'):
                prefered_ingredients.add(ps.stem(tag[0]))
 
    missing_temp_ings = prefered_ingredients - listed_ingredients

    with open('total_ingredients.pkl','rb') as f:
        total_ingredients = set(pickle.load(f))

    if len(total_ingredients.intersection((missing_temp_ings)))>0:
        print("\nOops...you are short of the following ingredients to prepare this recipe")
        print("\nMissing Ingredients : ",total_ingredients.intersection(missing_temp_ings))
    else:
        print("\nYou have all ingredients to prepare this recipe")

    for each in total_ingredients.intersection(missing_temp_ings):
        print(lemmatizer.lemmatize(each))



if __name__ == '__main__':
    iBotIntro()
    ingredients_query=get_input()
    recipe_id=get_Recipe(ingredients_query)
    if None!=recipe_id:
        get_Recipe_ingredients(recipe_id)
        print("Happy Cooking....\n")
        print("Don't forget to use Roomba to clean your kitchen")
    else:
        print("OOps...Not able to find the recipe with the ingredients you have...")
