#!/usr/bin/python
import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
import sys
import re

def striptags(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def load_taste(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find("script", {"data-schema-entity": "recipe"})
    for i in slugs.contents:
        data = json.loads(i)
    return data


def load_allrecipes(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find_all("script", {"type": "application/ld+json"})
    data = json.loads(striptags(str(slugs)))
    return data[0][1]

def load_bbcfood(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find_all("script", {"type": "application/ld+json"})
    elements = str(slugs).split('>')
    elements = elements[1].split('<')
    data = json.loads(elements[0])
    return data

def load_jamieoliver(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find_all("script", {"type": "application/ld+json"})
    data = json.loads(striptags(str(slugs)))
    return data[0]

def load_sugarfreediva(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find_all("script", {"type": "application/ld+json"})
    data = json.loads(striptags(str(slugs[0])))
    return data['@graph'][7]


def load_skel(url):
    recipesource = requests.get(url)
    source = BeautifulSoup(recipesource.text, features="html.parser")
    slugs = source.find_all("script", {"type": "application/ld+json"})

def convert_to_grams(ingredients):
    for i in ingredients:
        print(i)


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
recipe = sys.argv[1]
#result = load_taste(tasterecipe)
#convert_to_grams(result['recipeIngredient'])
#recipe = "https://www.allrecipes.com/recipe/60564/strawberry-cake-from-scratch/"
ingredients = get_ingredients(recipe)
convert_to_grams(ingredients['recipeIngredient'])
