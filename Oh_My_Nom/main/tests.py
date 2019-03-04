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
			template.loader.get_template("main/index.html")	
		except:
			self.fail("could not find index template, are you sure templates are being served?")
