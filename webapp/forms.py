from .models import Member
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    template_name = "form_snippet.html"
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        labels = {
            "username" : "Login",
            "email": "Email",
            "password": "Senha",
        }

        helptext_class = "block text-gray-500 text-sm mt-1"

        widgets ={
            "username" : forms.TextInput(attrs={"placeholder":"login", "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}), 
            "email" : forms.TextInput(attrs={"placeholder":"email", "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}), 
            "password" : forms.PasswordInput(attrs={"placeholder":"senha", "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}), 
        }

class ProfileForm(forms.ModelForm):
    template_name = "form_snippet.html"
    class Meta:
        model = Member
        fields = ['phone', 'birthday', 'address',  'suit', 'terms_agreed']

        labels = {
            "phone": "Telefone",
            "birthday": "Data de Nascimento",
            "address": "Endereço",
            "suit": "Voz",
            "terms_agreed": "Concordo com os termos e condições"
        }

        helptext_class = "block text-gray-500 text-sm mt-1"

        widgets ={ 
            "phone" : forms.TextInput(attrs={"placeholder":"(99)99999-9999", "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}), 
            "birthday" : forms.DateInput(attrs={"placeholder":"Dt. Nascimento", "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500", "type": "date"}), 
            "address" : forms.TextInput(attrs={"placeholder":"login", "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}), 
            "suit" : forms.Select(attrs={"placeholder":"login", "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}), 
        }