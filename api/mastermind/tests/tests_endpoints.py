from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Mastermind
from ..serializers import MastermindSerializer
from .factories import MastermindFactory
from random import randint
from django.test import TestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
import json

class EndpointTests(APITestCase):

	def setUp(self):
		self.user_payload = {
		'username':'admin',
		'password':'21Buttons'
		}
		self.valid_payload = {
			'name':'21 Button',
			'is_winner':False,
			'still_active':True,
			'match_time':'00:00:00'
		}
		
		self.invalid_payload = {
			'name':'21 Button',
			'winner':False,
			'still':True,
			'time':'00:00:00'
		}
		
		self.code_payload = {
			'code':'G-B-R-K',
			'match':1,
		}
		
	def test_get(self):
		"""Test endpoint to get a single game """
		client = APIClient()
		user = User(username='isaac', password='21Buttons')
		user.save()
		client.force_authenticate(user=user)
		game = MastermindFactory()
		game.save()
		response = client.get(reverse('get_game', kwargs={'pk': game.id}))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
		
	def test_get_all_games(self):
		"""Test endpoint to get all games """
		client = APIClient()
		response = client.get(reverse('get_all_games'))
		#get data from db
		games = Mastermind.objects.all()
		serializer = MastermindSerializer(games, many=True)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		#self.assertEqual(response.data, serializer.data)
		
		
	def test_create(self):
		""" Test endpoint to create a new game """
		client = APIClient()
		user = User(username='isaac', password='21Buttons')
		user.save()
		client.force_authenticate(user=user)
		response = client.post(
			reverse('post_new_game'),
			data=json.dumps(self.valid_payload),
			content_type='application/json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		
	def test_create_unauthorized(self):
		""" Test endpoint reject unauthotrized request on new game"""
		client = APIClient()
		response = client.post(
		reverse('post_new_game'),
		data=json.dumps(self.valid_payload),
		content_type='application/json'
		)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		
	def test_post_code(self):
		""" Test endpoint that receives a code from the code breaker"""
		client = APIClient()
		user = User(username='isaac', password='21Buttons')
		user.save()
		client.force_authenticate(user=user)
		game = MastermindFactory()
		game.save()
		response = client.post(
			reverse('post_code',kwargs={ "pk": game.id }),
			data=json.dumps(self.code_payload),
			content_type='application/json'
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
