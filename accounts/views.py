from django.shortcuts import render

# Create your views here.
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from website.models import Customer
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import PasswordReset
from accounts.forms import ForgotPasswordForm
# Create your views here.
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            print(form.errors)
            if form.is_valid():
               
                username_or_email = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
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
                user = form.save()  # Save the user instance

                # Create a corresponding Customer instance
                Customer.objects.create(
                    user=user,
                    name=user.username,  # Assign username as the name for example
                    email=user.email,    # Assign email from the user
                )
                
                messages.success(request, 'your signed up succesfully')
                return redirect('/')
            for key,value in form.error_messages.items():
                print(form.errors)
                messages.error(request, value)
        
        form = CustomUserCreationForm()
        return render(request,'accounts_templates/signup.html', {'form':form})
    else:
        return redirect('/')
            






def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                # Generate a random token and save it in the database
                token = get_random_string(length=32)
                reset_instance = PasswordReset.objects.create(user=user, token=token)
                # Send email with reset link containing the token
                reset_link = request.build_absolute_uri(f'/accounts/reset-password/{token}/')
                send_mail(
                    'Password Reset',
                    f'Click the link to reset your password: {reset_link}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )
                return render(request, 'registration/password_reset_email_sent.html')
            else:
                # Handle case where email does not exist in the database
                return render(request, 'registration/invalid_email.html')
    else:
        form = ForgotPasswordForm()
    return render(request, 'registration/forgot_password.html', {'form': form})
    



def reset_password(request, token):
    reset_instance = PasswordReset.objects.filter(token=token).first()
    if reset_instance and (timezone.now() - reset_instance.created_at).days < 1:
        if request.method == 'POST':
            new_password = request.POST.get('new_password')  # Replace 'new_password' with your password field name
            confirm_password = request.POST.get('confirm_password')  # Replace 'confirm_password' with your confirmation password field name

            if new_password == confirm_password:
                # Update the user's password and save
                user = reset_instance.user
                user.password = make_password(new_password)
                user.save()

                # Reset the token after successful password reset
                reset_instance.delete()  # Delete the token after successful password reset
                return render(request, 'registration/password_reset_successful.html')
            else:
                # Passwords don't match, render the reset password form again with an error message
                error_message = "Passwords do not match. Please try again."
                return render(request, 'registration/reset_password_form.html', {'error_message': error_message})
        else:
            return render(request, 'registration/reset_password_form.html')
    else:
        return render(request, 'registration/invalid_reset_link.html')