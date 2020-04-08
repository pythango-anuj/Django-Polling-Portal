from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('signin/', views.signinview, name='Signin'),
    path('signup/', views.signupview, name='Signup'),
    path('aboutus/', views.aboutus, name='About'),
    path('contact/', views.contact, name='Contact'),
    path('login/', views.loginview, name='Login'),
    path('register/', views.registerview, name='Register'),
    path('logout/',views.logoutview,name='Logout'),
    path('voting/', views.voting, name='Voting'),
    path('response/', views.save_response, name='response'),
]
