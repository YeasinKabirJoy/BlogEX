from .models import Blog,Tag
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def search_blog(request):

    search_text = ""

    if request.GET.get('search-text'):
        search_text = request.GET.get('search-text')
    tags = Tag.objects.filter(name__icontains=search_text)
    all_blogs = Blog.objects.distinct().filter(
        Q(title__icontains=search_text) |
        Q(description__icontains=search_text) |
        Q(owner__name__icontains=search_text) |
        Q(tags__in=tags)
    )

    return all_blogs,search_text


def paginate_blogs(request,blogs,result):
    page = request.GET.get('page')
    paginator = Paginator(blogs, result)
    try:
        all_blogs = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        all_blogs = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        all_blogs = paginator.page(page)

    left_index = int(page) - 2
    if left_index < 1:
        left_index = 1
    right_index = int(page) + 2
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages
    custom_range = range(left_index, right_index + 1)

    return all_blogs,custom_range
