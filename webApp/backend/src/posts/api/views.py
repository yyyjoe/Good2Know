from rest_framework.generics import ListAPIView, RetrieveAPIView
from posts.models import Post
from .serializers import PostsSerializer


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
