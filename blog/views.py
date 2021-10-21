from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication

from blog.models import Post, Category, Profile, Comment
from blog.permissions import IsAuthorOrReadOnly
from blog.serializers import UserSerilizer, PostSerializer, CategorySerializer, ProfileSerializer, CommentSerializer


def Index(request):
    return HttpResponse("Hello World")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerilizer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny, IsAuthorOrReadOnly]
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(auther=self.request.user)

    def perform_update(self, serializer):
        serializer.save(auther=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CategorySerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [permissions.AllowAny, IsAuthorOrReadOnly]
    authentication_classes = (TokenAuthentication,)
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CommentSerializer