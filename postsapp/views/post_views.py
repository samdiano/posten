from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models import Post
from ..serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from ..utils.jwt_utils import get_user_from_header

class Posts(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        posts = self.get_queryset()
        serializer = self.serializer_class(posts, many=True)
        response_data = {
            'status': 'success',
            'message': 'Posts retrieved successfully',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        user_id = get_user_from_header(request)
        request.data['author'] = user_id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status': 'success',
                'message': 'Post created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = {
            'status': 'fail',
            'message': 'Post creation failed',
            'data': serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"status": "fail", "message": f"Post with ID {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(post)
        return Response({"status": "success", "message": "Post retrieved successfully", "data": serializer.data})

    def patch(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"status": "fail", "message": f"Post with ID {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "Post updated successfully", "data": serializer.data})

        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"status": "fail", "message": f"Post with ID {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if user in post.likes.all():
        return Response({'message': 'Post already liked.'})
    else:
        post.likes.add(user)
        return Response({'message': 'Post liked.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        return Response({'message': 'Post unliked.'})
    else:
        return Response({'message': 'You have not liked this post.'})
