from django.db import models
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend


from .serializers import *
from .service import get_client_ip, MovieFilter
from .models import Movie


class MovieListView(generics.ListAPIView):      # Переделан на generics.ListAPIView
    '''вывод списка фильмов'''

    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
            # ratings - related name
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        # serializer = MovieListSerializer(movies, many=True)
        # return Response(serializer.data)

        return movies


class MovieDetailView(generics.RetrieveAPIView):   # класс переделан на generic class который сам обеспечивает поиск по pk
    '''Вывод информации о фильме'''

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    '''Ддобавление отзыва к фильму'''

    serializer_class = ReviewCreateSerializer



class AddStarRatingView(generics.CreateAPIView):
    '''Добавление рейтинга фильму'''


    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))



class ActorListView(generics.ListAPIView):
    '''Вывод списка актеров'''
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    '''Вывод полного описания актеров, режиссеров'''
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
