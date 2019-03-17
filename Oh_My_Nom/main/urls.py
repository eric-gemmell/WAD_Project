from main import views
from django.urls import path
from django.contrib import admin

app_name="main"
urlpatterns = [
	path("",views.index,name="index"),
	path("randomrecipes/",views.randomrecipes,name="randomrecipes"),
	path("hotrestaurants/",views.hotrestaurants,name="hotrestaurants"),
	path("hotrestaurantclicked/",views.hotrestaurantclicked,name="hotrestaurantclicked"),
	path("registersignin/",views.registersignin,name="registersignin"),
	path("signout/",views.signout,name="signout"),
	path("myplaces/",views.myplaces,name="myplaces"),
	path("myrecipes/",views.myrecipes,name="myrecipes"),
	path("test/",views.test,name="test"),
	path("admin/", admin.site.urls),
]

