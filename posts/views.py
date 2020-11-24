from .models import Post
from .serializers import CreatePostSerializer, ViewPostSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required

@api_view(['GET'])
def view_post(request, post_id):
    post_info = Post.objects.get(id=post_id)
    serializer = ViewPostSerializer(post_info)
    return Response(serializer.data)

@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()[0:10]
    serializer = ViewPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_required('management.post')
def create_post(request):
    post_info = request.data
    serializer = CreatePostSerializer(post_info)
    post_data = Post(title=serializer.data['title'], 
                    category=serializer.data['category'], 
                    content=serializer.data['content'])
    post_data.save()
    return Response(serializer.data)