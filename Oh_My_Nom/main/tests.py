from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles import finders
from django import template

class GeneralTests(TestCase):
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	def test_index_page_exists(self):
		response = self.client.get(reverse('main:index'))
		if(response.content == b""):
			self.fail("index page contains no content!")
	
	def test_templates_are_served(self):
		try:
			template.loader.get_template("main/test.html")	
		except:
			self.fail("could not find templates/main/test.html template, are you sure templates are being served?, maybe someone deleted the file...")

	def test_static_files_are_served(self):
		result = finders.find('images/test.jpg')
		if(result == None):
			self.fail("could not get images/test.jpg static file, are you they are served, or someone deleted the file?")

class ViewsTests(TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass


	def test_index_page_exists(self):
		response = self.client.get(reverse('main:index'))


	def test_hotrestaurants_page_exists(self):
		response = self.client.get(reverse('main:hotrestaurants'))

	def test_registersignin_page_exists(self):
		response = self.client.get(reverse('main:registersignin'))

	def test_randomrecipes_page_exists(self):
		response = self.client.get(reverse('main:randomrecipes'))

	def test_myrecipes_page_exists(self):
		response = self.client.get(reverse('main:myrecipes'))

	def test_myplaces_page_exists(self):
		response = self.client.get(reverse('main:myplaces'))


