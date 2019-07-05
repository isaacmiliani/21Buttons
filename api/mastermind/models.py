from django.conf import settings
from django.db import models


# Create your models here.

class Mastermind(models.Model):
	"""
	Mastermind Model
	Defines the attributes for a mastermind match
	"""
	name = models.CharField(max_length=255)
	codeBreaker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	is_winner = models.BooleanField()
	still_active = models.BooleanField()
	match_time = models.TimeField()
	game_code = models.CharField(max_length=255)
	
	def __str__(self):
		return self.name

	def get_results(self):
		return 'Winner: ' + self.name
		

class MatchResume(models.Model):
	"""
	Match Resume Model
	Defines the resume of a mastermind match
	"""

	match = models.ForeignKey('Mastermind', on_delete=models.CASCADE)
	code = models.CharField(max_length=30)
	code_response = models.CharField(max_length=30)
