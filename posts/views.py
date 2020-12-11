from .models import Post
from .serializers import CreatePostSerializer, ViewPostSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['GET'])
def view_post(request, post_id):
    post_info = Post.objects.get(id=post_id)
    serializer = ViewPostSerializer(post_info)
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()[0:10]
    serializer = ViewPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_required('posts.add_post', raise_exception=True)
def create_post(request):
    post_info = request.data
    serializer = CreatePostSerializer(post_info)
    post_data = Post(title=serializer.data['title'], 
                    category=serializer.data['category'], 
                    content=serializer.data['content'])
    post_data.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
