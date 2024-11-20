from django.urls import path, include
from . import views

urlpatterns = [
    path('tournaments/', views.tournament_list, name="tournaments_list"),
    path('tournaments/<int:pk>', views.tournament_detail, name="tournaments_detail"),
    path('join/<int:pk>', views.join_tournament, name="join_tournament"),
    path('leave/<int:pk>', views.leave_tournament, name="leave_tournament"),
]
