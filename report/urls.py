from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('tools/', tools, name='tools'),
    path('test/', test, name='test'),
    path('auth_check/', auth_check, name='auth_check'),
    path('profile/', profile, name="profile"),
    path('profile/edit/', edit_profile, name="edit_profile"),

    path('tools/excel/', excel, name='excel'),
    path('tools/debit/', debit, name='debit'),
    path('tools/delete_debtor/<int:debtor_id>/', delete_debtor, name='delete_debtor'),
    path('tools/edit_debtor/<int:debtor_id>/', edit_debtor, name='edit_debtor'),
    path('tools/debtor_debts/<int:debtor_id>', view_debts_that_debtor, name='view_debts_that_debtor'),
    path('tools/search/', search_debtors, name='search_debtors'),

    path('tools/list/', list_view, name='list'),
    path('tool/list/approve/<int:req_id>/', approve_request, name="approve_request"),
    path('tool/list/reject/<int:req_id>/', reject_request, name="reject_request"),
    path('tool/list/delete/<int:req_id>/', delete_request_product, name="delete_request"),

    path('tools/products/', products, name='products'),
    path('tools/products/details/<int:product_id>', product_details, name="product_details"),
    path('tools/products/edit/<int:product_id>', edit_product, name="edit_product"),
    path('tools/products/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('tools/products/search/', search_products, name='search_products'),
    path('tools/view_product/<int:product_id>', view_product, name='view_product'),

    path('warehouse/', warehouse, name='warehouse'),
    path('warehouse/stock/edit/<int:stock_id>', edit_stock, name="edit_stock"),
    path('warehouse/stock/delete/<int:stock_id>/', delete_stock, name='delete_stock'),


    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
