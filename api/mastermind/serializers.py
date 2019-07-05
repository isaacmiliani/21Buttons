from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Mastermind, MatchResume


class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

class MastermindSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Mastermind
		fields = '__all__'#('id', 'name', 'is_winner', 'still_active', 'match_time','game_code')

	def test_model_fields(self):
		"""Serializer data matches the Mastermind object for each field."""
		mastermind = MastermindFactory()
		for field_name in [
			'name', 'is_winner', 'still_active', 'match_time', 'game_code'
		]:
			self.assertEqual(
			serializer.data[field_name],
			getattr(mastermind, field_name)
		)
		
class MatchResumeSerializer(serializers.ModelSerializer):
	match = MastermindSerializer(many=False, read_only=True)
	match_id = serializers.IntegerField(write_only=True)

	class Meta:
		model = MatchResume
		fields = '__all__'
	
	code = serializers.CharField()
	code_response = serializers.CharField()

	
	def create(self, validated_data):
		"""
		Create and return a new `MatchResume` instance, given the validated data.
		"""
		return MatchResume.objects.create(**validated_data)
