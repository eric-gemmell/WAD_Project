import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Oh_My_Nom.settings')

import django
django.setup()
from main.models import Recipe, User, SavedRecipe

# List of dictionaries of recipes to be stored in the database 
def populate():
	recipes = [
	{"title": "Sweet Vegan Fajitas",
		"url":"https://www.theedgyveg.com/2016/04/20/easy-vegan-fajitas-dinner-15-minutes/"},
	{"title":"Meatballs",
		"url":"https://www.bbc.com/food/recipes/meatballs_with_tomato_70221"},
	{"title":"Toast Sandwich",
		"url":"https://www.vegrecipesofindia.com/bombay-toast-sandwich/"},
	{"title": "Potato soup",
		"url":"https://www.bbc.com/food/recipes/potatosoup_11631"},
	{"title":"Cajun Salmon",
		"url":"https://www.olivemagazine.com/recipes/fish-and-seafood/cajun-salmon-with-rosemary-sweet-potato-wedges/"},
	{"title":"Pesto Pasta",
		"url":"https://deliciouslyella.com/2017/04/23/classic-pesto-pasta/"},
	{"title": "Green Beans with Bacon",
		"url":"https://www.tasteofhome.com/recipes/quick-green-beans-with-bacon/"},
	{"title":"Slow Cooker Beef Stew",
		"url":"https://www.bbcgoodfood.com/recipes/slow-cooker-beef-stew"},
	{"title":"Chicken Curry",
		"url":"https://realfood.tesco.com/recipes/chicken-and-tomato-spiced-curry.html"},
	{"title": "Refried bean and cheese tamales with jalapeno salsa",
		"url":"https://www.bbc.com/food/recipes/refried_bean_and_cheese_05363"},
	{"title":"Feta, roasted red pepper and pine nut pancakes",
		"url":"https://www.bbc.com/food/recipes/feta_roasted_red_pepper_90674"},
	{"title":"Sachertorte",
		"url":"https://www.bbc.com/food/recipes/sachertorte_59630"},
	{"title": "Courgetti spaghetti",
		"url":"https://www.bbc.com/food/recipes/tomato_and_broccoli_08254"},
	{"title":"Minced beef pie",
		"url":"https://www.bbc.com/food/recipes/mincedbeefpie_89198"},
	{"title":"Crab and cod fishcakes with tomato salsa",
		"url":"https://www.bbc.com/food/recipes/crab_and_cod_fishcakes__15634"},
	{"title": "Lamb casserole with aubergine",
		"url":"https://www.bbc.com/food/recipes/lamb_casserole_with_94069"},
	{"title":"Egg-fried rice",
		"url":"https://www.bbc.com/food/recipes/eggfriedrice_67782"},
	{"title":"Creamy paprika chicken",
		"url":"https://www.bbc.com/food/recipes/panfriedpaprikachick_73735"},
	{"title":"Mac & Cheese",
		"url":"https://www.bbc.com/food/recipes/mac_n_cheese_70611"},
	{"title":"Mary Berry’s lasagne",
		"url":"https://www.bbc.com/food/recipes/mary_berrys_lasagne_al_16923"},
	]
	for recipe in recipes:
		add_recipe(recipe["title"],recipe["url"])

def add_recipe(title, url):
	r = Recipe.objects.get_or_create(title=title)[0]
	r.url = url
	r.save()
	return r

if __name__ == '__main__':
	print("Starting Noms population script...")
	populate()
