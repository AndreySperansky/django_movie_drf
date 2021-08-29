from rest_framework import serializers

from .models import Movie, Review, Rating, Actor

class FilterReviewListSerializer(serializers.ListSerializer):
    '''Фильтр комментариев только parent'''
    def to_representation(self, data):      # data это queryset
        data = data.filter(parent=None)
        return super().to_representation(data)



class RecursiveSerializer(serializers.Serializer):
    '''вывод рекурсивно children'''
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewCreateSerializer(serializers.ModelSerializer):
    '''Добавление отзыва'''
    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    '''Вывод отзыва'''
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer  # чтобы children не выводился дважды
        model = Review
        fields = ('name', 'text', 'children')


class ActorListSerializer(serializers.ModelSerializer):
    '''Вывод списка актеров и режиссеров'''
    class Meta:
        model = Actor
        fields = ("id", "name", "image")


class ActorDetailSerializer(serializers.ModelSerializer):
    '''Вывод полного описания актеров и режиссеров'''
    class Meta:
        model = Actor
        fields = "__all__"



class MovieListSerializer(serializers.ModelSerializer):
    '''Список фильмов'''
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ("id", "title", "tagline", "category", "rating_user", "middle_star")


class MovieDetailSerializer(serializers.ModelSerializer):
    '''Детали фильма'''

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    # directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    directors = ActorDetailSerializer(read_only=True, many=True)
    # actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = ActorDetailSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft",)


class CreateRatingSerializer(serializers.ModelSerializer):
    '''Добавлениие рэйтинга пользователем'''
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        # объект передается в  rating, а True или False передается в _
        return rating


