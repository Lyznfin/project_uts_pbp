from django.urls import path, include
from .views import Home, SignUp

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('sign-up', SignUp.as_view(), name='sign-up')
]
