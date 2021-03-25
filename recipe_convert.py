#!/usr/bin/python
import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
import sys
import re

# strip tags from the soup
def striptags(raw_html):
    cleanr = re.compile("<.*?>")
    return re.sub(cleanr, "", raw_html)


# load a recipe from taste.com.au
def load_taste(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find("script", {"data-schema-entity": "recipe"})
    for i in slugs.contents:
        data = json.loads(i)
    return data


# load a recipe from allrecipes.com - not allrecipes.com.au as it doesn't pack JSON
def load_allrecipes(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find_all("script", {"type": "application/ld+json"})
    data = json.loads(striptags(str(slugs)))
    return data[0][1]


# load from jamieoliver.com and bbc.co.uk
def load_jamieoliver(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find_all("script", {"type": "application/ld+json"})
    data = json.loads(striptags(str(slugs)))
    return data[0]


# load from sugarfreediva.com
def load_sugarfreediva(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find_all("script", {"type": "application/ld+json"})
    data = json.loads(striptags(str(slugs[0])))
    return data["@graph"][len(data["@graph"]) - 1]


# load epicurious..uses <li> tags instead of JSON
def load_epicurious(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    ingreds = source.find_all("li", {"itemprop": "ingredients"})
    data = {"recipeIngredient": []}
    for ingredient in ingreds:
        data["recipeIngredient"].append(striptags(str(ingredient)).strip())
    return data


# load allrecipes.com.au..uses <li> tags instead of JSON
def load_arau(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    ingreds = source.find_all("span", {"itemprop": "ingredients"})
    data = {"recipeIngredient": []}
    for ingredient in ingreds:
        data["recipeIngredient"].append(striptags(str(ingredient)))
    return data


# load nigella.com... uses <li> tags instead of JSON
def load_nigella(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    ingreds = source.find_all("li", {"itemprop": "recipeIngredient"})
    data = {"recipeIngredient": []}
    for ingredient in ingreds:
        data["recipeIngredient"].append(striptags(str(ingredient)))
    return data


# load sbs food


def load_sbs(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find("div", {"class": "field-name-field-ingredients"})
    data = {"recipeIngredient": []}
    for i in slugs.text.split("\n"):
        if i != "":
            data["recipeIngredient"].append(striptags(str(i)))
    return data


# load delicious.com.au
def load_delicious(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find("script", {"type": "application/ld+json"})
    return json.loads(striptags(str(slugs)))


# default skeleton for working out how to unpack the recipe
def load_skel(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find_all("script", {"type": "application/ld+json"})
    print(slugs)
    return json.loads(striptags(str(slugs)))


# will be the process to iterate ingredients and convert
def convert_to_grams(ingredients):
    for i in ingredients:
        print(i)


# work out which way we need to import the recipe
def get_ingredients(url):
    parts = url.split("/")
    if "taste.com.au" in parts[2]:
        return load_taste(recipe)
    elif "sugarfreediva" in parts[2]:
        return load_sugarfreediva(recipe)
    elif "bestrecipes" in parts[2]:
        return load_taste(recipe)
    elif "bbc.co.uk" in parts[2]:
        return load_jamieoliver(recipe)
    elif "jamieoliver" in parts[2]:
        return load_jamieoliver(recipe)
    elif "nigella.com" in parts[2]:
        return load_nigella(recipe)
    elif "allrecipes.com.au" in parts[2]:
        return load_arau(recipe)
    elif "allrecipes.com" in parts[2]:
        return load_allrecipes(recipe)
    elif "epicurious.com" in parts[2]:
        return load_epicurious(recipe)
    elif "sbs.com.au" in parts[2]:
        return load_sbs(recipe)
    elif "delicious.com.au" in parts[2]:
        return load_delicious(recipe)
    elif "goodfood.com.au" in parts[2]:
        return load_delicious(recipe)
    elif "recipetineats.com" in parts[2]:
        return load_sugarfreediva(recipe)
    elif "4ingredients.com.au" in parts[2]:
        return load_sugarfreediva(recipe)
    elif "livelighter.com.au" in parts[2]:
        return load_epicurious(recipe)
    else:
        return load_skel(recipe)


# taking recipe URL from commandline
recipe = sys.argv[1]

ingredients = get_ingredients(recipe)
convert_to_grams(ingredients["recipeIngredient"])
