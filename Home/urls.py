from django.urls import path
from .views import HomeView, PostDetailView, LoginView, LogoutView, Register, ProfileUpdateView, AboutView, ContactView, \
    DeleteAccountView, PostCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
    path('register/', Register.as_view(), name='register'),
    path('user/edit/', ProfileUpdateView.as_view(), name='edit_user'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('addpost/', PostCreateView.as_view(), name='create_post'),
]