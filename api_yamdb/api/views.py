from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filters import TitleFilterSet
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)
from .viewsets import CreateDeleteViewSet
from reviews.models import Category, Genre, Review, Title
from users.models import CustomUser
from users.permissions import IsAdminUserOrReadOnly, IsStaffOrAuthorOrReadOnly


class CategoryViewSet(CreateDeleteViewSet):
    """Вьюсет модели Катагория"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('id')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    lookup_field = 'slug'
    search_fields = ('=name',)
    permission_classes = [IsAdminUserOrReadOnly]


class GenreViewSet(CreateDeleteViewSet):
    """Вьюсет модели Жанр"""
    serializer_class = GenreSerializer
    queryset = Genre.objects.all().order_by('id')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    lookup_field = 'slug'
    search_fields = ('=name',)
    permission_classes = [IsAdminUserOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Произведение"""
    queryset = Title.objects.all().order_by('id')
    serializer_class = TitleSerializer
    filterset_class = TitleFilterSet
    filter_backends = (DjangoFilterBackend, )
    permission_classes = [IsAdminUserOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Отзыв"""
    serializer_class = ReviewSerializer
    permission_classes = [IsStaffOrAuthorOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        the_title = get_object_or_404(Title, id=title_id)
        return the_title.reviews.all().order_by('id')

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        the_title = get_object_or_404(Title, id=title_id)
        author = get_object_or_404(CustomUser, username=self.request.user)
        serializer.save(title=the_title, author=author)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Комментарий"""
    serializer_class = CommentSerializer
    permission_classes = [IsStaffOrAuthorOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        the_review = get_object_or_404(Review, id=review_id)
        return the_review.comments.all().order_by('id')

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        the_review = get_object_or_404(Review, id=review_id)
        author = get_object_or_404(CustomUser, username=self.request.user)
        serializer.save(review=the_review, author=author)
