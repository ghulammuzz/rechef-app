from django.urls import path
from .views import *

urlpatterns = [
    path('test/', TestView.as_view()),
    
    path('register/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    
]
