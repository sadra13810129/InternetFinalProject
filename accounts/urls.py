from django.urls import path
from accounts.views import *
app_name = 'accounts'

urlpatterns = [
    path('login/',login_view,name="login"),
    path('logout/',logout_view,name="logout"),
    path('signup/',signup_view,name="signup"),
    path('forgot-password/', forgot_password, name='forgot_password'),

    path('reset-password/<str:token>/', reset_password, name='reset_password'),
    
]

