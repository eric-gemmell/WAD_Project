# -*- coding: cp1252 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Oh_My_Nom.settings')

import django
django.setup()
from Nom.models import Category, Page

def populate():

	recipes_pages = [
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
                


	restaurant_pages = [
		{"title":"Paesano",
		"url":"https://paesanopizza.co.uk/"},
		{"title":"Topolabamba",
		"url":"https://www.topolabamba.com/"},
		{"title":"Ubiquitous Chip",
		"url":"https://www.ubiquitouschip.co.uk/"},
                
                {"title":"Doner Haus",
		"url":"https://www.donerhaus.uk/"},
		{"title":"Wagamama",
		"url":"https://www.wagamama.com/"},
		{"title":"Kimchi Cult!",
		"url":"http://www.kimchicult.com/"},

                {"title":"Baffo",
		"url":"https://www.baffo.co.uk/"},
		{"title":"Eusebi Deli",
		"url":"http://eusebideli.com/"},
		{"title":"Brel",
		"url":"https://www.brelbar.com/"},

                {"title":"Iberica",
		"url":"https://www.ibericarestaurants.com/"},
		{"title":"Left Bank",
		"url":"http://theleftbank.co.uk/"},
		{"title":"Halloumi Glasgow",
		"url":"http://www.halloumiglasgow.co.uk/#"},

                {"title":"Bread Meats Bread",
		"url":"http://www.breadmeatsbread.com/"},
		{"title":"Brgr",
		"url":"https://www.brgr-glasgow.com/"},

                {"title":"Cafe Andaluz",
		"url":"https://www.cafeandaluz.com/"},
		{"title":"Crab Shakk",
		"url":"http://www.crabshakk.com/"},
		{"title":"Wudon",
		"url":"http://www.wudon-noodlebar.co.uk/"},

                {"title":"Kelvin Pocket",
		"url":"http://kelvinpocket.co.uk/"},
		{"title":"Roast",
		"url":"http://www.roastglasgow.com/"},
		{"title":"Wudon",
		"url":"http://www.wudon-noodlebar.co.uk/"}
                ]

	cats = {"Recipes": {"pages": recipes_pages},
		"Restaurants": {"pages": restaurant_pages},
                }


	for cat, cat_data in cats.items():
		c = add_cat(cat)
		for p in cat_data["pages"]:
			add_page(c, p["title"], p["url"])

	for c in Category.objects.all():
		for p in Page.objects.filter(category=c):
			print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url):
	p = Page.objects.get_or_create(category=cat, title=title)[0]
	p.url=url
	p.save()
	return p

def add_cat(name):
	c = Category.objects.get_or_create(name=name)[0]
	c.save()
	return c

if __name__ == '__main__':
	print("Starting Noms population script...")
	populate()
