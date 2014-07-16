from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from gm.models import Manager, PredraftPick
from league.models import Player

@login_required
def home(request):

    try:
        manager = Manager.objects.get(user=request.user)
    except Manager.DoesNotExist:
        raise Http404

    teams = manager.leagueteam_set.all()
    return render_to_response("gm/home.html",
                              {'gm':manager,
                               'leagues':teams},
                              context_instance=RequestContext(request))

@login_required
def gm_rank(request):
    try:
        gm = Manager.objects.get(user=request.user.id)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == 'POST' and request.is_ajax:
        reset = request.POST.get("reset", False)
        if reset:
            predraft_picks = gm.predraftpick_set.all()
            predraft_picks.update(exclude=False)
            return HttpResponse('ok')

        ranking_list = request.POST.getlist("ranking_list[]")
        exclude_list = request.POST.getlist("exclude_list[]")

        gm.set_predraftpick_order(ranking_list)
        ranking_picks = PredraftPick.objects.filter(gm=gm, player__id__in=ranking_list)
        ranking_picks.update(exclude=False)

        exclude_picks = PredraftPick.objects.filter(gm=gm, player__id__in=exclude_list)
        exclude_picks.update(exclude=True)
        return HttpResponse('ok')

    init_predraft_list(gm)
    predraft_picks = gm.predraftpick_set.filter(exclude=False)
    exclude_picks = gm.predraftpick_set.filter(exclude=True)
    #csrf_token = csrf(request)
    return render_to_response('gm/gm_rank.html',
                              {'gm':gm,
                               'predraft_picks':predraft_picks,
                               'exclude_picks':exclude_picks,
                               },
                              context_instance=RequestContext(request))

def init_predraft_list(manager):
    players = Player.objects.all()

    for player in players:
        PredraftPick.objects.get_or_create(manager=manager, player=player)


