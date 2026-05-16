from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='list'),
    path('<int:pk>/', views.book_detail, name='detail'),
    path('add/', views.book_create, name='create'),
    path('<int:pk>/edit/', views.book_update, name='update'),
    path('<int:pk>/delete/', views.book_delete, name='delete'),
    path('<int:pk>/qr/', views.book_qr_code, name='qr_code'),
    path('<int:pk>/wishlist/toggle/', views.toggle_wishlist, name='toggle_wishlist'),
    path('my-wishlist/', views.my_wishlist, name='my_wishlist'),
]
