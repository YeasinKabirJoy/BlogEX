from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("blogs/", views.get_blogs, name="get-blogs"),
    path("blogs/<str:id>/", views.get_blog, name="get-blog"),
    path("blogs/<str:id>/vote", views.blog_vote, name="blog-vote"),
    path("remove-tag/", views.remove_tag),
]