from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from reservation.models import Restaurant, Table, Menu, Customer, Reservation, Order, Payment, Review, Promotion, LoyaltyProgram
from .serializers import RestaurantSerializer, TableSerializer, MenuSerializer, CustomerSerializer, ReservationSerializer, OrderSerializer, PaymentSerializer, ReviewSerializer, PromotionSerializer, LoyaltyProgramSerializer
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm


######## VISTE PER L'IMPLEMENTAZIONE DELLE FUNZIONALITÀ DELL'APP #######
# View per ottenere la lista dei ristoranti
class RestaurantList(View):
    def get(self, request):
        restaurants = Restaurant.objects.all()
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



######## VISTE PER LE REGISTRAZIONI ALL'APP ########
# View per la registrazione dell'utente generico
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redireziona all'URL di login dopo la registrazione
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

#aggiungi altri tipi di registrazioni...





