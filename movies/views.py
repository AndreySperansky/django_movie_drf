from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView



from .serializers import *
from .service import get_client_ip
from .models import Movie


class MovieListView(APIView):
    '''вывод списка фильмов'''

    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            # 1-st method
            # rating_user=models.Case(
            #     models.When(ratings__ip=get_client_ip(request),then=True),
            #     # rating - таблица, ip поле таблицы
            #         default=False,
            #         output_field=models.BooleanField()
            #     ),

            # 2-nd method
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
            # ratings - related name
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
         )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    '''Вывод информации о фильме'''

    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)

class ReviewCreateView(APIView):
    '''Ддобавление отзыва к фильму'''
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    '''Добавление рейтинга фильму'''

    # Метод перенесен в отдельный файл service.py
    #==================================================================#
    # def get_client_ip(selfself, request):
    #     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    #     if x_forwarded_for:
    #         ip = x_forwarded_for.split(',')[0]
    #     else:
    #         ip = request.META.get('REMOTE_ADDR')
    #     return ip

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
