"""
URL configuration for AppResto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from reservation.views import CreateCustomerView, CreateMenu, CreateReservation, CreateRestaurant, CreateTable, DeleteMenu, DeleteRestaurant, DeleteTable, FilterMenuView, RestaurantList, TableListView, UpdateMenu, UpdateRestaurant, UpdateTable
from geopy import distance
from geopy import Point


urlpatterns = [
    #FUNZIONALITÀ APPLICAZIONE
    #tabella ristorante
    path('admin/', admin.site.urls),
    path('listrestaurants/', RestaurantList.as_view(), name='restaurant-list'),
    path('restaurants/', CreateRestaurant.as_view(), name = 'create-restaurant'),
    path('deleterestaurants/<int:restaurant_id>/', DeleteRestaurant.as_view(), name = 'delete-restaurant'),
    path('updaterestaurants/<int:restaurant_id>/', UpdateRestaurant.as_view(), name = 'update-restaurant'),
    
    #tabella tavolo
    path('tables/', CreateTable.as_view(), name = 'create-table'),
    path('deletetable/<int:table_id>/', DeleteTable.as_view(), name = 'delete-table'),
    path('updatetable/<int:table_id>/', UpdateTable.as_view(), name = 'update-table'),
    path('listtable/<int:restaurant_id>/', TableListView.as_view(), name = 'table-list'),

    #tabella menu
    path('menus/', CreateMenu.as_view(), name='create-menu'),
    path('deletemenu/<int:menu_id>/', DeleteMenu.as_view(), name='delete-menu'),
    path('updatemenu/<int:menu_id>/', UpdateMenu.as_view(), name='update-menu'),
    path('listmenu/', FilterMenuView.as_view(), name='menu-list'),

    # tabella reservations
    path('reservations/', CreateReservation.as_view(), name='create-reservation'),
    
    #tabella customer
    path('customer/', CreateCustomerView.as_view(), name = 'create-customer'),
    
    #aggiungi altre funzionalità...

    #GESTIONE AUTENTICAZIONI
    path('login/', auth_views.LoginView.as_view(), name='login'), # percorso autenticazione utente generico
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #aggiungi altri tipi di accesso...

]
