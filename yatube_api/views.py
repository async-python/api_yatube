from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import PostSerializer, CommentSerializer
from posts.models import Post, Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        post = self.get_post(**kwargs)
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    def update(self, request, **kwargs):
        post = self.get_post(**kwargs)
        serializer = self.get_serializer(
            post, data=request.data, partial=True)
        if serializer.is_valid():
            if post.author != request.user:
                return Response(
                    serializer.errors, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, **kwargs):
        post = self.get_post(**kwargs)
        if post.author != request.user:
            return Response(request.data, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(request.data, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_post(**kwargs):
        return get_object_or_404(Post, id=kwargs['pk'])


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(post_id=kwargs['post_id'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        comment = self.get_comment(**kwargs)
        serializer = self.get_serializer(comment)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_comment(**kwargs)
        if comment.author != request.user:
            return Response(request.data, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(request.data, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        comment = self.get_comment(**kwargs)
        serializer = self.get_serializer(
            comment, data=request.data, partial=True)
        if serializer.is_valid():
            if comment.author != request.user:
                return Response(
                    serializer.errors, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_comment(**kwargs):
        return get_object_or_404(
            Comment, id=kwargs['pk'], post_id=kwargs['post_id'])
