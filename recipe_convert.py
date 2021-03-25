#!/usr/bin/python
import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
import sys
import re

#strip tags from the soup
def striptags(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


#load a recipe from taste.com.au
def load_taste(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find("script", {"data-schema-entity": "recipe"})
    for i in slugs.contents:
        data = json.loads(i)
    return data

#load a recipe from allrecipes.com - not allrecipes.com.au as it doesn't pack JSON
def load_allrecipes(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find_all("script", {"type": "application/ld+json"})
    data = json.loads(striptags(str(slugs)))
    return data[0][1]

#load from jamieoliver.com and bbc.co.uk
def load_jamieoliver(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find_all("script", {"type": "application/ld+json"})
    data = json.loads(striptags(str(slugs)))
    return data[0]

#load from sugarfreediva.com
def load_sugarfreediva(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find_all("script", {"type": "application/ld+json"})
    data = json.loads(striptags(str(slugs[0])))
    return data['@graph'][7]

#default skeleton for working out how to unpack the recipe
def load_skel(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find_all("script", {"type": "application/ld+json"})

#will be the process to iterate ingredients and convert
def convert_to_grams(ingredients):
    for i in ingredients:
        print(i)

#work out which way we need to import the recipe
def get_ingredients(url):
    parts = url.split('/')
    if  'allrecipes' in parts[2]:
        result = load_allrecipes(recipe)
    elif  'taste.com.au' in parts[2]:
        result = load_taste(recipe)
    elif  'sugarfreediva' in parts[2]:
        result = load_sugarfreediva(recipe)
    elif 'bestrecipes' in parts[2]:
        result = load_taste(recipe)
    elif 'bbc.co.uk' in parts[2]:
        result = load_jamieoliver(recipe)
    elif 'jamieoliver' in parts[2]:
        result = load_jamieoliver(recipe)
    else:
        result = load_skel(recipe)
    return result

#taking recipe URL from commandline
recipe = sys.argv[1]

ingredients = get_ingredients(recipe)
convert_to_grams(ingredients['recipeIngredient'])
