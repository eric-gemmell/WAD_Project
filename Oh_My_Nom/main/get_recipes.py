from django.db import models
from main.models import Category
from main.models import Page
from main import views
import random


def getRecipes():
	recipes = []
	
	category_list = Category.objects
	
	#get random numbers and pick those indices as recipes (range of how many recipes you have)
	randList = random.sample(range(1,20),5)
	for i in randList:
		recipes += category_list["Recipes"]["pages"][i]
		print (recipes)
	return recipes
	
	