from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('tools/', tools, name='tools'),
    path('test/', test, name='test'),

    path('tools/excel/', excel, name='excel'),
    path('tools/debit/', debit, name='debit'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
