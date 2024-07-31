from django.urls import path

from articles.views import ArticleListCreateView, ArticleDetailView


urlpatterns = [
    path('', ArticleListCreateView.as_view(), name='articles'),
    path('<int:pk>', ArticleDetailView.as_view(), name='articles_detail'),
]
