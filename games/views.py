from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from games.forms import PlayForm

from api.models import Game, Play, Post
from api.views import Week

from libs.gfycat import gfycat

def scoreboard(request, week_id='R_1'):
    wc_dict = week_choices_dict()
    context = {}
    context['week_choices_tuples'] = zip(wc_dict['week_choices'], wc_dict['week_choice_ids'])
    context['games'] = Week.games_for_weekid(week_id)

    return render(request, 'games/scoreboard.html', context)

def scoreboard_table(request, week_id):
    context = {'games': Week.games_for_weekid(week_id)}
    return render(request, 'games/scoreboard_table.html', context)

def game_detail(request, gamekey):

    try:
        game = Game.objects.get(gamekey=gamekey)
    except:
        raise Http404
    context = dict()

    if request.method == 'GET':
        if 'edit' in request.GET.keys():
            play_id = request.GET['play_id']
            play = Play.objects.get(id=play_id)
            play_form = PlayForm(game.away_team, game.home_team, instance=play)
            context['edit'] = True
            context['play'] = play
        else:
            play_form = PlayForm(game.away_team, game.home_team)

    if request.method == 'POST':
        if 'delete' in request.POST.keys():
            play_id = request.POST['play_id']
            play = Play.objects.get(id=play_id)
            play.delete()
            play_form = PlayForm(game.away_team, game.home_team)
        else:
            if 'edit' in request.POST.keys():
                print 'get form'
                play_id = request.POST['play_id']
                print play_id
                play = Play.objects.get(id=play_id)
                context['edit'] = True
                context['play'] = play
                play_form = PlayForm(game.away_team, game.home_team, request.POST, instance=play)
            else:
                play_form = PlayForm(game.away_team, game.home_team, request.POST)
            # check whether it's valid:
            if play_form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                play = play_form.save(commit=False)

                if play_form.cleaned_data['gfy_url']:
                    mp4_url = gfycat().more(play_form.cleaned_data['gfy_url']).get('mp4Url')
                    play.mp4_url = mp4_url

                play.gamekey = gamekey
                play.post = Post.objects.create(text=play.text)
                play.save()
                if 'edit' in context:
                    return HttpResponseRedirect(reverse('game-detail', kwargs={'gamekey':gamekey}))

                play_form = PlayForm(game.away_team, game.home_team, instance=play)
            else:
                print 'not valid'
                print play_form.errors
            # return HttpResponseRedirect(reverse('game-detail', gamekey=gamekey))


    context['game'] = game
    context['plays'] = Play.objects.filter(gamekey=gamekey).order_by('-quarter', 'time')
    context['play_form'] = play_form
    print context

    return render(request, 'games/game_detail.html', context)

def week_choices_dict():
    return {
        "week_choices" : [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17"
        ],
        "week_choice_ids" : [
            "R_1",
            "R_2",
            "R_3",
            "R_4",
            "R_5",
            "R_6",
            "R_7",
            "R_8",
            "R_9",
            "R_10",
            "R_11",
            "R_12",
            "R_13",
            "R_14",
            "R_15",
            "R_16",
            "R_17",
        ]
    }
