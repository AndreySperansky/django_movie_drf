from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *



urlpatterns = format_suffix_patterns([
    path("movie/", MovieViewSet.as_view({'get': 'list'})),
    path("movie/<int:pk>/", MovieViewSet.as_view({'get': 'retrieve'})),
    path("review/", ReviewCreateViewSet.as_view({'post': 'create'})),
    path("rating/", AddStarRatingViewSet.as_view({'post': 'create'})),
    path('actor/', ActorsViewSet.as_view({'get': 'list'})),
    path('actor/<int:pk>/', ActorsViewSet.as_view({'get': 'retrieve'})),
])


# urlpatterns = [
#     path('movie/', MovieListView.as_view()),
#     path('movie/<int:pk>/', MovieDetailView.as_view()),
#     path('review/', ReviewCreateView.as_view()),
#     path('rating/', AddStarRatingView.as_view()),
#     path('actors/', ActorListView.as_view()),
#     path('actors/<int:pk>/', ActorDetailView.as_view()),
# ]