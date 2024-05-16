from django.urls import path
from applications import views

urlpatterns = [
    path('', views.index),
    path('encrypt', views.api_encrypt_image, name='api_encrypt_image'),
    path('decrypt', views.api_decrypt_image, name='api_decrypt_image'),
]
