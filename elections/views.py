from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404


from .models import Candidate, Poll, Choice

import datetime

from django.db.models import Sum

def index(request):

    candidates = Candidate.objects.all()
    """
    str = ""

    for candidate in candidates:
        str += "<p>{} 기호 {}번 ({})<br />".format(candidate.name, candidate.party_number, candidate.area)
        str += candidate.introduction +"</p>"
    return HttpResponse(str)
    """

    context = {'candidates' : candidates} #context에 모든 후보에 대한 정보를 저장
    return render(request, 'elections/index.html', context) # context로 html에 모든 후보에 대한 정보를 전달

def candidates(request, name):
    candidate = get_object_or_404(Candidate, name=name)
    """
    try:
        candidate = Candidate.objects.get(name = name)
    except:
        raise Http404
        #return HttpResponseNotFound("없는 페이지입니다.")
    """
    return HttpResponse(candidate.name)


def areas(request, area):
    today = datetime.datetime.now()
    # 에러 처리
    try:
        poll = Poll.objects.get(area=area, start_date__lte=today, end_date__gte=today)
        candidates = Candidate.objects.filter(area = area)
    except:
        poll = None
        candidates = None

    context = {'candidates' : candidates, 'area':area, 'poll':poll}
    return render(request, 'elections/area.html',context)


def polls(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    selection = request.POST['choice']

    try:
        choice = Choice.objects.get(poll_id=poll_id, candidate_id=selection)
        choice.votes += 1
        choice.save()
    except:
        choice = Choice(poll_id=poll_id, candidate_id=selection, votes=1)
        choice.save()
    return HttpResponseRedirect("/areas/{}/results".format(poll.area))

def results(request, area):

    candidates = Candidate.objects.filter(area = area)
    polls = Poll.objects.filter(area = area)
    poll_results = []
    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date

        total_votes = Choice.objects.filter(poll_id=poll.id).aggregate(Sum('votes'))

        # print("#########",total_votes)

        result['total_votes'] = total_votes['votes__sum']

        # 각 후보의 지지율 rates in favors
        rates = []
        for candidate in candidates:
            # 어떤 후보의 득표가 하나도 없다면
            try:
                choice = Choice.objects.get(poll_id=poll.id, candidate_id=candidate.id)
                rates.append(round(choice.votes*100/result['total_votes'],1))
            except:
                rates.append(0)
        result['rates'] = rates
        



        poll_results.append(result)

    context = {'candidates':candidates, 'area':area,
    'poll_results' : poll_results}
    return render(request, 'elections/result.html', context)