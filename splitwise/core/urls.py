from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trips/create/', views.create_trip, name='create_trip'),
    path('trips/<int:pk>/', views.trip_detail, name='trip_detail'),
    path('trips/<int:trip_id>/add-participant/',
         views.add_participant, name='add_participant'),
    path('trips/<int:trip_id>/add-expense/',
         views.add_expense, name='add_expense'),
    path('expenses/<int:expense_id>/edit/',
         views.edit_expense, name='edit_expense'),
    path('expenses/<int:expense_id>/delete/',
         views.delete_expense, name='delete_expense'),
]
