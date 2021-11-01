from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog.views import Index, PostViewSet, CategoryViewSet, ProfileViewSet, CommentViewSet, UserViewSet, getUser, \
    likePost, disLikePost

# PostList, PostDetails

# post_list, post_details

router = DefaultRouter()
router.register('posts', PostViewSet,'Posts')
router.register('categories', CategoryViewSet,'Categories')
router.register('profiles', ProfileViewSet,'Profiles')
router.register('comments', CommentViewSet,'Comments')
router.register('users', UserViewSet, basename='users')


urlpatterns=[
    path('', Index),
    path('api/getuser/', getUser.as_view()),
    path('api/likepost/', likePost.as_view()),
    path('api/dislikepost/', disLikePost.as_view()),
    path('api/', include(router.urls)),

]

