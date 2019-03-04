from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles import finders


class GeneralTests(TestCase):
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	def test_index_page_exists(self):
		response = self.client.get(reverse('index'))
		if(response.content == b""):
			self.fail("index page contains no content!")


