from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import IntegerField
from django.core.validators import MaxValueValidator, MinValueValidator


class MyUser(AbstractUser):
    """Кастомная модель Пользователя"""
    class RoleChoice(models.TextChoices):
        """Класс с вариантами выбора прав доступа."""
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    role = models.CharField(
        max_length=50,
        choices=RoleChoice.choices,
        default=RoleChoice.USER,
        verbose_name='Права доступа'
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='Биография'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты',
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель Категории Произведения"""
    name = models.CharField(max_length=50, verbose_name='Название категории')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['-id', ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель Жанра Произведения"""
    name = models.CharField(max_length=50, verbose_name='Название жанра')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель Произведения"""
    name = models.CharField(
        max_length=100,
        db_index=True,
        unique=True,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Год выпуска',
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        # through='GenreTitle',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET(''),
        related_name='category',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ['-id', ]
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель Отзыва на Произведение"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв',
        help_text='Напишите свой отзыв',
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    score = IntegerField(
        validators=[
            MinValueValidator(
                1, 'Оценка должна быть от 1 до 10'),
            MaxValueValidator(
                10, 'Оценка должна быть от 1 до 10')
        ],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']
        # один юзер - один отзыв
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='review_is_exists'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    """Модель Комменатрия к Отзыву на Произведение"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
        help_text='Введите текст комментария'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:20]


# class GenreTitle(models.Model):
#     """Промежуточная модель Жанр-Произведение"""
#     title_id = models.ForeignKey(Title, models.SET(''),)
#     genre_id = models.ForeignKey(Genre, models.SET(''),)

#     class Meta:
#         verbose_name = 'Жанр-Произведение'
#         verbose_name_plural = 'Жанр-Произведение'
