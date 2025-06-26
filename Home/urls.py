from django.urls import path
from .views import HomeView, PostDetail, Login, Logout, Register

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('register', Register.as_view(), name='register'),
]