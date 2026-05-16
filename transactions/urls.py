from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('issue/', views.issue_book, name='issue_book'),
    path('return/<int:record_id>/', views.return_book, name='return_book'),
    path('records/', views.record_list, name='record_list'),
    path('my-books/', views.my_borrowed_books, name='my_books'),
    path('export-pdf/', views.export_transactions_pdf, name='export_pdf'),
]
