from rest_framework import serializers
from .models import Restaurant, Table, Menu, Customer, Reservation, Order, Payment, Review, Promotion, LoyaltyProgram

class RestaurantSerializer(serializers.ModelSerializer):
    available_tables = serializers.SerializerMethodField()

    def get_available_tables(self, obj):
        return Table.objects.filter(restaurant=obj, is_available=True).count()

    class Meta:
        model = Restaurant
        fields = '__all__'

        available_tables = serializers.IntegerField()

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'

class LoyaltyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyProgram
        fields = '__all__'

