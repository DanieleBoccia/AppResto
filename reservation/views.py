from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse, HttpResponse
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

        serializer = RestaurantSerializer(restaurants, many=True)
        return JsonResponse(serializer.data, safe=False)

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






