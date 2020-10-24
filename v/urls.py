from django.urls import path, include
from v import views
from v.views import *

urlpatterns = [
    path('home', home, name="home"),
    path('movie', movie, name="movie"),
    path('background', set_background, name="background"),
    path('help', help_page, name="help"),
    path('music', music, name="music"),
    path('music/search', music_search, name="music_search"),
    path('movie/search', movie_search, name="movie_search"),
    path('movie/home', movie_home, name="movie_home"),
    path('movie/<int:movie_id>', movie_page, name="movie_page"),
    path('movie/<int:movie_id>/play-<int:play_id>', movie_play, name="movie_play"),
    path('/', home, name="none_1"),
    path('', home, name="none_2"),
    path('baidu/translate', translate, name="translate"),
    path('url', data_post, name="url_post")

]
