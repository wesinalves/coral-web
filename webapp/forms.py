from .models import Member, User
from django import forms

class RegisterForm(forms.ModelForm):
    template_name = "form_snippet.html"
    class Meta:
        model = Member
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
        fields = ['first_name', 'last_name', 'email', 'phone', 'birthday', 'address',  'suit']

        labels = {
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "email": "Email",
            "phone": "Telefone",
            "birthday": "Data de Nascimento",
            "address": "Endereço",
            "suit": "Voz",
        }

        helptext_class = "block text-gray-500 text-sm mt-1"

        widgets ={ 
            "first_name" : forms.TextInput(attrs={"placeholder":"Nome", "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}), 
            "last_name" : forms.TextInput(attrs={"placeholder":"Sobrenome", "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}), 
            "email" : forms.EmailInput(attrs={"placeholder":"Email", "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}), 
            "phone" : forms.TextInput(attrs={"placeholder":"(99)99999-9999", "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}), 
            "birthday" : forms.DateInput(attrs={"placeholder":"Dt. Nascimento", "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500", "type": "date"}, format=('%Y-%m-%d')), 
            "address" : forms.TextInput(attrs={"placeholder":"Endereço", "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}), 
            "suit" : forms.Select(attrs={"placeholder":"Naipe", "class":"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}), 
        }    