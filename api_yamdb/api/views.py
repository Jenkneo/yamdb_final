from rest_framework import filters
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

from .filters import TitleFilter
from reviews.models import Title, Category, Genre, Review
from .serializers import (
    ForAdminSerializer, ForUserSerializer, TitleReadSerializer,
    CategorySerializer, GenreSerializer, TitleWriteSerializer,
    ReviewSerializer, CommentSerializer,
    UserRegistrationSerializer, UserGetTokenSerializer
)
from .permissions import IsAdminOrModeratorOrAuthor, IsAdminOrReadOnly, IsAdmin

from api_yamdb.settings import EMAIL_HOST_USER


User = get_user_model()


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ForAdminSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,))
    def me(self, request, pk=None):
        user = self.request.user
        if request.method == 'GET':
            serializer = ForUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = ForUserSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegistrationViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    """Вьюсет для создания обьектов класса User."""

    queryset = User.objects.all()

    def create(self, request):
        """Создание объекта User и отправка кода на email"""
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if User.objects.filter(email=request.data['email']).exists():
            username = User.objects.get(email=request.data['email']).username
            if username != request.data['username']:
                message = 'Пользователь с таким email уже зарегестрирован'
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=request.data['username']).exists():
            email = User.objects.get(username=request.data['username']).email
            if email != request.data['email']:
                message = 'Пользователь с таким username уже зарегестрирован'
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=EMAIL_HOST_USER,
            recipient_list=(user.email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserGetTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вьюсет для получения токена."""

    queryset = User.objects.all()
    serializer_class = UserGetTokenSerializer

    def create(self, request, *args, **kwargs):
        """Отправка токена по коду из email."""
        serializer = UserGetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Код подтверждения невалиден'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    """Создает произведение или возвращает список произведений"""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleWriteSerializer
        return TitleReadSerializer


class ListPostDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(ListPostDeleteViewSet):
    """Получает категорию или список категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(ListPostDeleteViewSet):
    """Получает жанр или список жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Получает список всех отзывов"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrAuthor,)

    def get_title(self):
        return get_object_or_404(
            Title.objects.prefetch_related('reviews'),
            pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Получает список всех комментариев к отзыву"""
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModeratorOrAuthor,)

    def get_review(self):
        return get_object_or_404(
            Review.objects.prefetch_related('comments'),
            pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
