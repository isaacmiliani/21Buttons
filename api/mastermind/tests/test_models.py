from django.test import TestCase

from ..models import Mastermind, MatchResume
from .factories import MastermindFactory, MatchResumeFactory


class MastermindTestCase(TestCase):
	def test_create(self):
		"""Test to create a new game."""
		game = MastermindFactory()
		game.save()
		self.assertEqual(Mastermind.objects.count(), 1)
		self.assertEqual(str(game), game.name)
		
	def test_delete(self):
		"""Test delete a game from database."""
		game = MastermindFactory()
		game.save()
		self.assertEqual(Mastermind.objects.count(), 1)
		game.delete()
		self.assertEqual(Mastermind.objects.count(), 0)
		
class MatchResumeTestCase(TestCase):
	def test_create(self):
		""" Test to save a play """
		match_resume = MatchResumeFactory()
		self.assertEqual(MatchResume.objects.count(), 1)
