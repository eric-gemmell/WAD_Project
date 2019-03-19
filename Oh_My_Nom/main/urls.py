from main import views
from django.urls import path
from django.contrib import admin

app_name="main"
urlpatterns = [
	path("",views.index,name="index"),
	#random recipes pages
	path("randomrecipes/",views.randomrecipes,name="randomrecipes"),
	path("myrecipes/",views.myrecipes,name="myrecipes"),
	#restaurants pages
	path("hotrestaurants/",views.hotrestaurants,name="hotrestaurants"),
	path("hotrestaurantclicked/",views.hotrestaurantclicked,name="hotrestaurantclicked"),
	path("myplaces/",views.myplaces,name="myplaces"),
	path("getlocation/",views.getlocation,name="getlocation"),
	path("getrestaurants/",views.getrestaurants,name="getrestaurants"),
	#general pages
	path("registersignin/",views.registersignin,name="registersignin"),
	path("signout/",views.signout,name="signout"),
	#testing pages
	path("test/",views.test,name="test"),
	path("admin/", admin.site.urls),
]

