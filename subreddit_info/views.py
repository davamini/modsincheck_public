from django.shortcuts import render
from django.http import HttpResponse
from .models import Subreddit
import datetime
import json
# Create your views here.


def get_subreddit_date(subreddit_name):
    try:
        subreddit_objects = Subreddit.objects.filter(name=subreddit_name)
        curr_subreddit = subreddit_objects.latest('date').__dict__
        scores = []
        dates = []
        for record in subreddit_objects:
            dates.append(str((record.date + datetime.timedelta(days=1)).isoformat()))
            scores.append(record.score)
        context = {
            'name': subreddit_name,
            'scores': json.dumps(scores),
            'dates': json.dumps(dates),
            'most_recent_score': curr_subreddit['score'],
            }
        return context

    except Subreddit.DoesNotExist:
        return None

def subreddit_info_page(request, subreddit_name):
    context = get_subreddit_date(subreddit_name)

    return render(request=request, template_name= 'subreddit_info.html', context=context)