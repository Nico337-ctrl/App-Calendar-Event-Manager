from django.urls import path
from dashboard.views import *

urlpatterns = [
path('signup/', SessionSignup.as_view(), name='signup'),
path('logout/', SessionLogout.as_view(), name='logout'),
path('signin/', SessionSignin.as_view(), name='signin'),
]