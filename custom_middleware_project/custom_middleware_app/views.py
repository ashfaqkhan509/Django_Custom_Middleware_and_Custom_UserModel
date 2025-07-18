from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return HttpResponse("User Registered successfully.")
    else:
        form = RegisterForm()
    return render(request, "custom_middleware_app/user_register.html", {'form': form})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                return HttpResponse("Invalid credentials.")
    else:
        form = LoginForm()
    return render(request, "custom_middleware_app/user_login.html", {"form": form})


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect(login)

@login_required(login_url="login")
def home_page_view(request):
    return HttpResponse(f"Hello, Welcom to the Django Custom User Model Testing App")
















# class RegisterView(View):
#     def get(self, request):
#         form = RegisterForm()
#         return render(request, "custom_middleware_app/user_register.html", {'form': form})

#     def post(self, request):
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             login(request, user)
#             return HttpResponse("User Registered successfully.")
#         return render(request, "custom_middleware_app/user_register.html", {'form': form})


# class LoginView(View):
#     def get(self, request):
#         form = LoginForm()
#         return render(request, "custom_middleware_app/user_login.html", {"form": form})

#     def post(self, request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data["email"]
#             password = form.cleaned_data["password"]
#             user = authenticate(request, email=email, password=password)
#             if user:
#                 login(request, user)
#                 return redirect("home")
#             else:
#                 return HttpResponse("Invalid credentials.")
#         return render(request, "custom_middleware_app/user_login.html", {"form": form})


# class LogoutView(LoginRequiredMixin, View):
#     login_url = 'login'

#     def post(self, request):
#         logout(request)
#         return redirect('login')


# class HomePageView(LoginRequiredMixin, View):
#     login_url = 'login'

#     def get(self, request):
#         return HttpResponse("Hello, Welcome to the Django Custom User Model Testing App")
