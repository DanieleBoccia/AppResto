from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.views import View
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from reservation.forms import CustomerForm
from reservation.models import Restaurant, Table, Menu, Customer, Reservation, Order, Payment, Review, Promotion, LoyaltyProgram
from .serializers import RestaurantSerializer, TableSerializer, MenuSerializer, CustomerSerializer, ReservationSerializer, OrderSerializer, PaymentSerializer, ReviewSerializer, PromotionSerializer, LoyaltyProgramSerializer
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomerForm
from geopy import distance
from geopy import Point


######## VISTE PER L'IMPLEMENTAZIONE DELLE FUNZIONALITÀ DELL'APP #######

# View per ottenere la lista dei ristoranti
class RestaurantList(ListView):
    def get(self, request):
        query_params = request.GET

        name = query_params.get('name')
        cuisine_type = query_params.get('cuisine_type')
        city = query_params.get('city')
        address = query_params.get('address')
        description = query_params.get('description')
        restaurant_type = query_params.get('restaurant_type')
        quarter = query_params.get('quarter')
        user_latitude = request.GET.get('latitude', None)
        user_longitude = request.GET.get('longitude', None)

        restaurants = Restaurant.objects.all()

        if name:
            restaurants = restaurants.filter(name__icontains=name)
        
        if cuisine_type:
            restaurants = restaurants.filter(cuisine_type__icontains=cuisine_type)
        
        if city:
            restaurants = restaurants.filter(city__icontains=city)
        
        if address:
            restaurants = restaurants.filter(address__icontains=address)
        
        if description:
            restaurants = restaurants.filter(description__icontains=description)
        
        if restaurant_type:
            restaurants = restaurants.filter(restaurant_type__icontains=restaurant_type)
        
        if quarter:
            restaurants = restaurants.filter(quarter__icontains=quarter)
        
        #ricerca tramite geolocalizzazione
        if user_latitude and user_longitude:
          user_location = Point(latitude=float(user_latitude), longitude=float(user_longitude))
          radius = 5  # Raggio di 5 chilometri
          filtered_restaurants = []
          for restaurant in restaurants:
            restaurant_location = Point(latitude=restaurant.latitude, longitude=restaurant.longitude)
            if distance.distance(user_location, restaurant_location).km <= radius:
              filtered_restaurants.append(restaurant)
          restaurants = filtered_restaurants


        serializer = RestaurantSerializer(restaurants, many=True)
        return JsonResponse(serializer.data, safe=False)
    
# View per la creazione di un nuovo ristorante
@method_decorator(csrf_exempt, name='dispatch')
class CreateRestaurant(View):
    def post(self, request):
        data = json.loads(request.body)
        serializer = RestaurantSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=400)

# View per l'eliminazione del ristorante    
@method_decorator(csrf_exempt, name='dispatch')
class DeleteRestaurant(View):
    def delete(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            restaurant.delete()
            return JsonResponse({'message': 'Restaurant deleted successfully.'}, status=204)
        except Restaurant.DoesNotExist:
            return JsonResponse({'error': 'Restaurant not found.'}, status=404)
        
# View per l'aggiornamento del ristorante
@method_decorator(csrf_exempt, name='dispatch')
class UpdateRestaurant(View):
    def put(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            data = json.loads(request.body)
            serializer = RestaurantSerializer(restaurant, data=data)
            
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            
            return JsonResponse(serializer.errors, status=400)
        
        except Restaurant.DoesNotExist:
            return JsonResponse({'error': 'Restaurant not found.'}, status=404)
        
# View per la creazione di un nuovo tavolo
@method_decorator(csrf_exempt, name='dispatch')
class CreateTable(View):
    def post(self, request):
        data = json.loads(request.body)
        serializer = TableSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=400)

# View per l'eliminazione del tavolo    
@method_decorator(csrf_exempt, name='dispatch')
class DeleteTable(View):
    def delete(self, request, table_id):
        try:
            table = Table.objects.get(id=table_id)
            table.delete()
            return JsonResponse({'message': 'Table deleted successfully.'}, status=204)
        except Table.DoesNotExist:
            return JsonResponse({'error': 'Table not found.'}, status=404)
        
# View per l'aggiornamento del tavolo
@method_decorator(csrf_exempt, name='dispatch')
class UpdateTable(View):
    def put(self, request, table_id):
        try:
            table = Table.objects.get(id=table_id)
            data = json.loads(request.body)
            serializer = TableSerializer(table, data=data)
            
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            
            return JsonResponse(serializer.errors, status=400)
        
        except Table.DoesNotExist:
            return JsonResponse({'error': 'Table not found.'}, status=404)

# View per ottenere lista tavoli associati al ristorante        
class TableListView(ListView):
    model = Table

    def get_queryset(self):
        queryset = super().get_queryset()

        # Ottenere l'ID del ristorante dai parametri dell'URL
        restaurant_id = self.kwargs['restaurant_id']

        # Filtrare i tavoli per l'ID del ristorante
        queryset = queryset.filter(restaurant_id=restaurant_id)

        # Verificare i parametri dell'URL per la disponibilità e la privacy
        is_available = self.request.GET.get('available')
        is_private = self.request.GET.get('private')

        if is_available and is_private:
            is_available = is_available.lower() == 'true'
            is_private = is_private.lower() == 'true'
            # Filtrare i tavoli per disponibilità e privacy
            queryset = queryset.filter(is_available=is_available, is_private=is_private)
        elif is_available:
            is_available = is_available.lower() == 'true'
            # Filtrare solo per disponibilità
            queryset = queryset.filter(is_available=is_available)
        elif is_private:
            is_private = is_private.lower() == 'true'
            # Filtrare solo per privacy
            queryset = queryset.filter(is_private=is_private)

        return queryset

    def render_to_response(self, context, **response_kwargs):
        # Serializzare i risultati in formato JSON
        data = [{'table_number': table.table_number, 'capacity': table.capacity,  'description': table.description} for table in context['object_list']]
        return JsonResponse(data, safe=False)

    def dispatch(self, request, *args, **kwargs):
        # Verificare se i parametri dell'URL sono validi
        if 'available' in request.GET and request.GET['available'].lower() not in ['true', 'false']:
            return HttpResponseBadRequest("Invalid value for 'available' parameter.")

        if 'private' in request.GET and request.GET['private'].lower() not in ['true', 'false']:
            return HttpResponseBadRequest("Invalid value for 'private' parameter.")

        return super().dispatch(request, *args, **kwargs)
    
# View per la creazione di un nuovo menu
class CreateMenu(View):
    def post(self, request):
        data = json.loads(request.body)
        serializer = MenuSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=400)

#View per l'aggiornamento del menu    
class UpdateMenu(View):
    def put(self, request, menu_id):
        data = json.loads(request.body)
        menu = Menu.objects.get(pk=menu_id)
        serializer = MenuSerializer(menu, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        
        return JsonResponse(serializer.errors, status=400)

#View per la cancellazione di un menu    
class DeleteMenu(View):
    def delete(self, request, menu_id):
        try:
            menu = Menu.objects.get(pk=menu_id)
            
            # Controllo se è stata fornita l'opzione per eliminare tutto il menu
            delete_all = request.GET.get('delete_all', False)
            
            if delete_all:
                # Elimina tutto il menu del ristorante
                restaurant_id = menu.restaurant_id
                Menu.objects.filter(restaurant_id=restaurant_id).delete()
                message = 'All menu items for the restaurant have been deleted.'
            else:
                # Elimina solo il menu specifico
                menu.delete()
                message = 'Menu item deleted successfully.'
            
            return JsonResponse({'message': message}, status=200)
        except Menu.DoesNotExist:
            return JsonResponse({'error': 'Menu not found'}, status=404)

# View per filtrare i menu secondo le proprie esigenze
class FilterMenuView(View):
    def get(self, request, restaurant_id):
        is_vegetarian = request.GET.get('vegetarian', False)
        is_gluten_free = request.GET.get('gluten_free', False)
        sort_by = request.GET.get('sort_by', None)
        
        menu_items = Menu.objects.filter(restaurant_id=restaurant_id)
        
        if is_vegetarian:
            menu_items = menu_items.filter(is_vegetarian=True)
        
        if is_gluten_free:
            menu_items = menu_items.filter(is_gluten_free=True)
        
        if sort_by == 'price_asc':
            menu_items = menu_items.order_by('price')
        elif sort_by == 'price_desc':
            menu_items = menu_items.order_by('-price')
        
        data = {
            'menu_items': list(menu_items.values())
        }
        
        return JsonResponse(data, status=200)
    

# View per creare una nuova prenotazione
@method_decorator(csrf_exempt, name='dispatch')
class CreateReservation(View):
    def post(self, request):
        data = json.loads(request.body)
        serializer = ReservationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# View per la creazione di un nuovo Customer
@method_decorator(csrf_exempt, name='dispatch')
class CreateCustomerView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'create_customer.html'
    success_url = reverse_lazy('customer_detail')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


#aggiungi altre funzionalità...



########   VISTE PER I LOGIN #######
# View per l'autenticazione dell'utente generico
@login_required
def protected_api_view(request):
    # Questa vista richiederà l'autenticazione
    # Restituisce una risposta JSON
    data = {'message': 'Questa è una risorsa protetta.'}
    return JsonResponse(data)

#aggiungi altri tipi di accesso






