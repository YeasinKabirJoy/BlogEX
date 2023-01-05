from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from blogs.models import Blog,Review,Tag
from .serializer import BlogSerializer,TagSerializer


@api_view(['GET'])
def get_blogs(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_blog(request,id):
    blogs = Blog.objects.get(id=id)
    serializer = BlogSerializer(blogs,many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blog_vote(request,id):
    blog = Blog.objects.get(id=id)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(owner=user,blog=blog)

    review.vote = data["vote"]
    review.save()
    blog.get_vote_count

    serializer = BlogSerializer(blog)
    return Response(serializer.data)


@api_view(['DELETE'])
def remove_tag(request):
    tagId = request.data['tag']
    blogId = request.data['blog']

    blog = Blog.objects.get(id=blogId)
    tag = Tag.objects.get(id=tagId)
    blog.tags.remove(tag)
    return Response("Tag was removed")

