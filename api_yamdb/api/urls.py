from django.urls import path, include
from rest_framework import routers

from .views import (
    UserRegistrationViewSet, UserGetTokenViewSet, TitleViewSet,
    CategoryViewSet, GenreViewSet, ReviewViewSet, CommentViewSet,
    MyUserViewSet
)


v1_router = routers.DefaultRouter()
v1_router.register(r'users', MyUserViewSet, basename='users')
v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/token/', UserGetTokenViewSet.as_view({'post': 'create'})),
    path('auth/signup/', UserRegistrationViewSet.as_view(
        {'post': 'create'}
    )),
]
