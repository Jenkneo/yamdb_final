from rest_framework import serializers, status
import datetime as dt
from django.contrib.auth import get_user_model

from reviews.models import Review, Comment, Title, Category, Genre


User = get_user_model()


class UserRegistrationSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя"""
    username = serializers.SlugField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'email', 'role')

    def validate(self, data):
        """Запрет на использование me, и повторных username и email"""
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать username "me" запрещено'
            )
        return data


class UserGetTokenSerializer(serializers.Serializer):
    """Сериализатор для объекта класса User при получении токена JWT."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class ForUserSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role')
        read_only_fields = ('role', 'email')


class ForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализация произведения при чтении."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(TitleReadSerializer):
    """Сериализация произведения при записи в БД."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if year <= value:
            raise serializers.ValidationError('Год выпуска больше текущего!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация отзыва"""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

    def validate(self, data):
        request_method = self.context.get('request').method
        if request_method == 'POST':
            author = self.context.get('request').user
            title_id = self.context.get('view').kwargs.get('title_id')
            reviews = author.reviews.all()
            if reviews.filter(title_id=title_id).exists():
                raise serializers.ValidationError(
                    detail='Вы уже делали ревью на это произведение!',
                    code=status.HTTP_400_BAD_REQUEST)
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация комментария"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
