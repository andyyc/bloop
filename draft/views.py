# Create your views here.
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from gm.models import Manager

@login_required
def gm_rank(request):
    try:
        gm = Manager.objects.get(user=request.user.id)
    except Manager.ObjectDoesNotExist:
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
    return render_to_response('league/gm_rank.html',
                              {'gm':gm,
                               'predraft_picks':predraft_picks,
                               'exclude_picks':exclude_picks,
                               },
                              context_instance=RequestContext(request))