from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from blog.models import Post, Category, Profile, Comment
from blog.permissions import IsAuthorOrReadOnly, UserPermission
from blog.serializers import UserSerilizer, PostSerializer, CategorySerializer, ProfileSerializer, CommentSerializer
from django.core.mail import send_mail

def Index(request):
    return HttpResponse("Hello World")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerilizer
    permission_classes = (UserPermission,)
    authentication_classes = (TokenAuthentication,)

class getUser(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serilizer = UserSerilizer(request.user)
        return Response(serilizer.data)

class likePost(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        userID = request.data["user_id"]
        postID = request.data["post_id"]
        user = User.objects.get(id=userID)
        post = Post.objects.get(id=postID)
        if (post.likes.add(user)):
            # send_mail(
            #     'Subject here',
            #     'Here is the message.',
            #     'songl08@wairaka.com',
            #     ['gabriel_sl19798@hotmail.com'],
            #     fail_silently=False,
            # )
            post.save()

            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)

class disLikePost(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # send_mail(
    #     'Subject here',
    #     'Here is the message.',
    #     'songl08@wairaka.com',
    #     ['gabriel_sl19798@hotmail.com'],
    #     fail_silently=False,
    # )
    def patch(self, request):

        userID = request.data["user_id"]
        postID = request.data["post_id"]
        user = User.objects.get(id=userID)
        post = Post.objects.get(id=postID)
        if (post.likes.remove(user)):

            post.save()

            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)

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