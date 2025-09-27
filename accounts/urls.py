from django.urls import path

from accounts.views import RegisterCreateView, LoginFormView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
]