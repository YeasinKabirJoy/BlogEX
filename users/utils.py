from django.db.models import Q
from .models import Profile,Skill
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


def search_profile(request):
    search_text = ""

    if request.GET.get('search-text'):
        search_text = request.GET.get('search-text')

    skills = Skill.objects.filter(name__icontains=search_text)
    all_profile = Profile.objects.distinct().filter(Q(name__icontains=search_text)
                                                    | Q(short_intro__icontains=search_text) |
                                                      Q(skill__in=skills)
                                                    )
    return all_profile,search_text


def paginate_profiles(request,profiles,result):
    page = request.GET.get('page')
    paginator = Paginator(profiles, result)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = int(page) - 2
    if left_index < 1:
        left_index = 1
    right_index = int(page) + 2
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages
    custom_range = range(left_index, right_index + 1)

    return profiles,custom_range
