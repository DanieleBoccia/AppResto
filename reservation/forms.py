from django import forms
from .models import Customer

# Form per la creazione del Customer
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'address', 'city', 'country', 'telephone_number', 'email']