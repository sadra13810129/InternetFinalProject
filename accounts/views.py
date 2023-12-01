from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from accounts.forms import CustomUserCreationForm

from django.urls import reverse_lazy

# Create your views here.
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            print(form.errors)
            if form.is_valid():
               
                username_or_email = form.cleaned_data.get('usernameOrEmail')
                password = form.cleaned_data.get('password')
                print(username_or_email,password)
                user = authenticate(request, username=username_or_email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')

            messages.error(request, 'your username,email or password is invalid')
            form = AuthenticationForm()
            return render(request, 'accounts_templates/login.html', {'form': form})
        else:
            form = AuthenticationForm()
        return render(request, 'accounts_templates/login.html', {'form': form})
    else:
        return redirect('/')

    
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/accounts/login')

def signup_view(request):
    if not request.user.is_authenticated: 
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'your signed up succesfully')
                return redirect('/')
            
            for key,value in form.error_messages.items():
                messages.error(request, value)
        
        form = CustomUserCreationForm()
        return render(request,'accounts_templates/signup.html', {'form':form})
    else:
        return redirect('/')
    
    
def custom_404(request, exception):
    return render(request, '404.html', status=404)
    