from django.conf.urls import patterns, include, url
from games import views

urlpatterns = patterns('',
    url(r'^scoreboard/$', 'games.views.scoreboard', name='scoreboard'),
    url(r'^scoreboard/(?P<week_id>\w+)$', 'games.views.scoreboard', name='scoreboard'),
    url(r'^scoreboard-table/(?P<week_id>\w+)$', 'games.views.scoreboard_table', name='scoreboard_table'),
    url(r'^game-detail/(?P<gamekey>\w+)$', 'games.views.game_detail', name='game-detail'),
)
