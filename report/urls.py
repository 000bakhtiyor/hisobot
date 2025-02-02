from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('tools/', tools, name='tools'),
    path('test/', test, name='test'),

    path('tools/excel/', excel, name='excel'),
    path('tools/debit/', debit, name='debit'),
    path('tools/delete_debtor/<int:debtor_id>/', delete_debtor, name='delete_debtor'),
    path('tools/edit_debtor/<int:debtor_id>/', edit_debtor, name='edit_debtor'),
    path('tools/debtor_debts/<int:debtor_id>', view_debts_that_debtor, name='view_debts_that_debtor'),
    path('tools/search', search_debtors, name='search_debtors'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
