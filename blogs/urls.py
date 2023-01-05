from django.urls import path
from . import views
urlpatterns = [
    path("blogs/", views.blogs, name="all-blogs"),
    path("blog/<slug:slug>/", views.single_blog, name="single-blog"),
    path("add-blog/", views.add_blog, name="add-blog"),
    path("update-blog/<slug:slug>/", views.update_blog, name="update-blog"),
    path("delete-blog/<str:id>/", views.delete_blog, name="delete-blog"),
]