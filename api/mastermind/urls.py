from django.conf.urls import url
from . import views

urlpatterns = [
	url(
		r'^api/v1/games/(?P<pk>[0-9]+)/plays/',
		views.post_code,
		name='post_code'
	),
	url(
		r'^api/v1/games/(?P<pk>[0-9]+)/',
		views.get_game,
		name='get_game'
	),
	url(
		r'^api/v1/games/all/',
		views.get_all_games,
		name='get_all_games'
	),
	url(
		r'^api/v1/games/',
		views.post_new_game,
		name='post_new_game'
	)
]
