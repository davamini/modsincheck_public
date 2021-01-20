from django.shortcuts import render
from django.http import HttpResponse
from .models import Mod
from subreddit_info.models import Subreddit
import json 
import datetime
from django.forms.models import model_to_dict 


def get_mod_data(mod_name):
    """
    Returns mod_data based on mod_name.

    Args:
        mod_name ([str]): The mod name.
    Returns:
        A dictionary containg mod_data if mod is
        in database. Else returns None.
    """
    try:
        mod_objects = Mod.objects.filter(name=mod_name)
        curr_mod = mod_objects.latest('date').__dict__
        scores = []
        dates = []
        for record in mod_objects:
            dates.append(str((record.date + datetime.timedelta(days=1)).isoformat()))
            scores.append(record.score)
        subreddits_moderated = curr_mod['subreddits_moderated']
        account_created = curr_mod['account_created']
        context = {
            'name': mod_name,
            'subreddit': curr_mod['subreddit'],
            'scores': json.dumps(scores),
            'dates': json.dumps(dates),
            'most_recent_score': curr_mod['score'],
            'subreddits_moderated': json.loads(subreddits_moderated),
            'account_created': account_created,
            }
        return context

    except Mod.DoesNotExist:
        return None

def mod_info_page(request, mod_name):
    """
    Returns the mod_info page based on mod_name
    """ 
    context = get_mod_data(mod_name)

    if context != None:
        return render(request=request, template_name='mod_info/mod_info.html', context=context)

    return render(request=request, template_name="mod_info/not_found.html", context={'name': mod_name})

def home_page(request):
    """
    Returns the home page
    """
    mods = [i[0] for i in Mod.objects.values_list('name').distinct()]
    subreddits = [i[0] for i in Subreddit.objects.values_list('name').distinct()]
    mod_subreddit_dict = {mod_name: Mod.objects.filter(name=mod_name).latest('date').__dict__['subreddit'] for mod_name in mods}
    orderd_by_score = Mod.objects.order_by('-score')
    curr_year = datetime.date.today().year
    curr_month = datetime.date.today().month
    #max_date = Mod.objects.latest('date').date
    filtered = orderd_by_score.filter(date__year=str(curr_year), 
                                   date__month=str(curr_month).zfill(2))
    top_3 = []
    count = 0
    for mod in filtered:
        if count == 3:
            break
        elif mod.name not in top_3:
            top_3.append(mod.name)
            count += 1
 
    top_3_dict = dict()
    for mod in enumerate(top_3):
        name = f"mod_{mod[0]}"
        top_3_dict[name] = get_mod_data(mod[1])
        del top_3_dict[name]['account_created']
        del top_3_dict[name]['subreddits_moderated']
    
    mod_subreddit_lst = []
    for mod in mods:
        mod_subreddit_lst.append({'name': mod, 'mod_or_subreddit': 'moderator'})
    for subreddit in subreddits:
        mod_subreddit_lst.append({'name': subreddit, 'mod_or_subreddit': 'subreddit'})
    top_3_dict['mod_lst'] = mods
    top_3_dict['auto_complete_data'] = json.dumps(mod_subreddit_lst)

    return render(request=request, template_name="homepage.html", context=top_3_dict)
