from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class GenCatField(serializers.SlugRelatedField):
        def to_representation(self, value):
            return {"name": value.name, "slug": value.slug}

    genre = GenCatField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True
    )
    category = GenCatField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True
    )

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)

    def validate(self, data):
        method = self.context['request'].method
        user = self.context['request'].user
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        if (method == 'POST'
                and user.reviews.filter(title_id=title_id).exists()):
            raise serializers.ValidationError(
                "Нельзя писать более одного отзыва на одно произведение!")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author',)
