from django.http import Http404
from django.shortcuts import render
from games.forms import PlayForm

from api.models import Game, Play
from api.views import Week, week_choices_dict

def scoreboard(request):
    wc_dict = week_choices_dict()
    context = {}
    context['week_choices_tuples'] = zip(wc_dict['week_choices'], wc_dict['week_choice_ids'])
    context['games'] = Week.games_for_weekid('PR_0')


    return render(request, 'games/scoreboard.html', context)

def scoreboard_table(request, week_id):
    context = {'games': Week.games_for_weekid(week_id)}
    return render(request, 'games/scoreboard_table.html', context)

def game_detail(request):
    gamekey = request.GET.get('gamekey')
    try:
        game = Game.objects.get(gamekey=gamekey)
    except:
        raise Http404
    context = dict()
    context['plays'] = Play.objects.filter(gamekey=gamekey).order_by('-quarter', 'time')
    context['play_form'] = PlayForm(game.away_team, game.home_team)
    print context
    return render(request, 'games/game_detail.html', context)