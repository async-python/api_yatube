from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .serializers import PostSerializer
from posts.models import User, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        post = Post.objects.get(id=id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            if post.author != request.user:
                return Response(serializer.errors,
                                status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        post = Post.objects.get(id=id)
        if post.author != request.user:
            return Response(request.data, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(request.data, status=status.HTTP_204_NO_CONTENT)
