from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile
import datetime
from main.models import Recipe, Rating, UserProfile, Rating
from django.contrib.auth.models import User

class RatingForm(forms.ModelForm):
    # user = models.ForeignKey(User)
    # recipe = models.ForeignKey(Recipe)
    date = forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.time())
    description = forms.CharField(max_length=100,help_text="Enter your rating.")
    #dishType = forms.CharField(max_length=100)
    #price = forms.CharField(max_length=100)
    #fanciness = forms.CharField(max_length=100)
    #firstDate = forms.CharField(max_length=100)
    #lazyNight = forms.CharField(max_length=100)
    #difficulty = forms.CharField(max_length=100)
    #dishType = forms.CharField(max_length=100)
    #price = forms.CharField(max_length=100)
    #veggie = forms.CharField(max_length=100)
    overall = forms.CharField(max_length=100)
    
    
    # an inline class to provide additional information on the form.
    class Meta:
        model = Rating
        # exclude foreign keys
        exclude = ("user", "recipe")

 
