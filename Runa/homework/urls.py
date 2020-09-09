from django.urls import path
from homework import views

urlpatterns = [
    path('categories/', views.Categories.as_view()),
    path('categories/<int:pk>/', views.CategoryDetail.as_view()),
]