from django.urls import path

from accounts.views import LoginView, LogoutView, RegisterAuthorView, RegisterView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('register/author', RegisterAuthorView.as_view(), name='register_author'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
