import factory
import json
import random
from factory import DjangoModelFactory
from faker import Factory
from django.contrib.auth import get_user_model
from ..models import Mastermind, MatchResume


faker = Factory.create()
class UserFactory(factory.DjangoModelFactory):
	"""
	UserFactory Model
	Defines the attributes for a mastermind match
	"""
	class Meta:
		model = get_user_model()
	
	
	username = faker.name() + '_' + faker.last_name()
	email = faker.email()
	
class MastermindFactory(factory.DjangoModelFactory):
	"""
	Mastermind Model
	Defines the attributes for a mastermind match
	"""
	class Meta:
		model = Mastermind
		
	name = faker.name() + "'s Battle"
	codeBreaker =  factory.SubFactory(UserFactory)
	is_winner = bool(random.getrandbits(1))
	still_active = False 
	match_time = faker.time(pattern="%H:%M:%S", end_datetime=None)
	game_code =  'G-R-B-P'
	
	
class MatchResumeFactory(factory.DjangoModelFactory):
	"""Mastermind Model
	Defines the attributes for a mastermind play
	"""
	
	class Meta:
		model = MatchResume
		
	match = factory.SubFactory(MastermindFactory)
	code =  faker.name()
	code_response =  faker.name()
	
