from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, RegisterForm, ContactForm, UserForm, PostForm
from .models import Post, ContactMessage, Category
from django.core.mail import EmailMessage
from django.contrib.auth.forms import PasswordChangeForm

class HomeView(ListView):
    model = Post
    template_name = 'Home/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    ordering = ['-created']


class PostDetailView(DetailView):
    model = Post
    template_name = 'Home/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        if post.category:
            related = Post.objects.filter(category=post.category).exclude(id=post.id)[:3]
        else:
            related = Post.objects.exclude(id=post.id)[:3]
        context['related_posts'] = related
        return context


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'Home/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
        return render(request, 'Home/login.html', {'form': form})


class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'Home/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            login(request, user)
            return redirect('home')
        return render(request, 'Home/register.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
        return render(request, 'Home/edit_user.html', {
            'user_form': user_form,
            'password_form': password_form,
        })

    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if 'update_user' in request.POST:
            if user_form.is_valid():
                user_form.save()
                return redirect('home')

        if 'change_password' in request.POST:
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user)
                return redirect('home')

        return render(request, 'Home/edit_user.html', {
            'user_form': user_form,
            'password_form': password_form,
        })


class AboutView(View):
    def get(self, request):
        return render(request, 'Home/about.html', {})


class ContactView(LoginRequiredMixin, View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'Home/contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ContactMessage.objects.create(
                name = cd['name'],
                email = cd['email'],
                subject = cd['subject'],
                message = cd['message'],
            )

            email = EmailMessage(
                subject=cd['subject'],
                body=f"Name: {cd['name']}\nEmail: {cd['email']}\n\nMessage:\n{cd['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.DEFAULT_FROM_EMAIL],
            )
            email.encoding = 'utf-8'
            email.send(fail_silently=False)

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        return render(request, 'Home/contact.html', {'form': form})


class DeleteAccountView(View):
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            logout(request)
            user.delete()
        return redirect('home')


class PostCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        categories = Category.objects.all()
        return render(request, 'Home/post_create.html', {'form': form, 'categories': categories})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        categories = Category.objects.all()
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
        return render(request, 'Home/post_create.html', {'form': form, 'categories': categories})