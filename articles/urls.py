from django.urls import path

from articles.views import PrivateDetailView, PrivateListCreateView, PublicDetailView, PublicListView


urlpatterns = [
    path('public', PublicListView.as_view(), name='public'),
    path('public/<int:pk>', PublicDetailView.as_view(), name='public_detail'),
    path('private', PrivateListCreateView.as_view(), name='private'),
    path('private/<int:pk>', PrivateDetailView.as_view(), name='private_detail'),
]
