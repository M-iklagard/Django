import json

from django.forms.models import ModelForm
from django.forms import Form
from django.contrib.auth.models import User
from django import forms
import requests

class RegForm(ModelForm):
    """Форма реєстрація"""
    class Meta:
        model = User
        fields= ["username", "password", "email", "first_name", "last_name"]
        labels = {
            "username": "",
            "password": "",
            "email": "",
            "first_name": "",
            "last_name": "",
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "логін", "class": "form-input"}),
            "password": forms.PasswordInput(attrs={"placeholder": "пароль", "class": "form-input"}),
            "email": forms.EmailInput(attrs={"placeholder": "електронна пошта", "class": "form-input"}),
            "first_name": forms.TextInput(attrs={"placeholder": "ім'я", "class": "form-input"}),
            "last_name": forms.TextInput(attrs={"placeholder": "прізвище", "class": "form-input"}),
        }
        # прибирає допоміжний текст
        help_texts = {"username": None}

class AuthForm(ModelForm):
    """Форма авторизації"""
    class Meta:
        model = User
        fields= ["username", "password"]
        help_texts = {"username": None}

        labels = {
            "username": "",
            "password": "",
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "логін", "class": "form-input"}),
            "password": forms.PasswordInput(attrs={"placeholder": "пароль", "class": "form-input"}),
        }


def get_cities():
    """Повертає всі міста"""
    API_KEY = "b65cd870b67d4a926d45dbf41ee20872"
    URL = "https://api.novaposhta.ua/v2.0/json/"

    data = {
                "apiKey": API_KEY,
                "modelName": "Address",
                "calledMethod": "getCities"
            }

    request = requests.post(url=URL, json=data)

    data = request.json()
    result = []
    for key, value in data.items():
        if key == "data":
            for city in value:
                if "Ref" and "Description" in city.keys():
                    result.append([city["Ref"], city["Description"]])
                else:
                    continue
    return result

def get_wh(ref):
    """Повертає склади за Ref міста"""
    API_KEY = "b65cd870b67d4a926d45dbf41ee20872"
    URL = "https://api.novaposhta.ua/v2.0/json/"

    data = {
        "apiKey": API_KEY,
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "methodProperties": {
            "CityRef": f"{ref}"
        }
    }

    request = requests.post(url=URL, json=data)

    data = request.json()
    result = []
    for key, value in data.items():
        if key == "data":
            for warehouse in value:
                if "CityRef" and "Description" in warehouse.keys():
                    result.append([warehouse["CityRef"], warehouse["Description"]])
                else:
                    continue
    return result


class OrderForm(Form):
    cities = get_cities()
    warehouses = []
    city = forms.ChoiceField(choices=cities,  widget=forms.Select(attrs={"id": "city","required":True, "class":"city"}), label="Місто")
    warehouse = forms.ChoiceField(choices=warehouses, widget=forms.Select(attrs={"id": "warehouse", "required":True,"class":"warehouse"}), label="Відділення")


class BioForm(Form):
    ful_name = forms.CharField(label="Ім'я отримувача", required=True, widget=forms.TextInput(attrs={'id': 'full_name', "class":"full_name"}))
    surname = forms.CharField(label="Прізвище отримувача", required=True, widget=forms.TextInput(attrs={'id': 'surname', "class":"surname"}))
    patronymic = forms.CharField(label="Побатькові отримувача", required=True, widget=forms.TextInput(attrs={'id': 'patronymic', "class":"patronymic"}))