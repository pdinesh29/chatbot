from django.urls import path
from . import views

app_name = 'chat'  # Define the app namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('create_room/', views.create_room, name='create_room'),
    path('room/<uuid:room_id>/', views.room, name='room'),
    path('join_room/<uuid:room_id>/', views.join_room, name='join_room'),
    path('leave_room/<uuid:room_id>/', views.leave_room, name='leave_room'),
    path('search/', views.search_rooms, name='search_rooms'),
]
