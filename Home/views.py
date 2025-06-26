from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from .models import Post


class HomeView(ListView):
    model = Post
    template_name = 'Home/post_list.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'Home/post_detail.html'
    context_object_name = 'post'


class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'Home/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username or Password is incorrect')
            return render(request, 'Home/login.html', {'form': form})

class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'Home/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            user = User.objects.create_user(username, email, password)
            login(request, user)
            return redirect('home')
        return render(request, 'Home/register.html', {'form': form})



class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('home')



