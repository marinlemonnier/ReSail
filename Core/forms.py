from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Item, ItemImage, User
from django.forms import inlineformset_factory

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone_number", "profile_picture")


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'title', 'description', 'price', 'currency', 
            'item_quality', 'country', 'city', 'neighborhood', 
            'trade_type', 'category' # J'ai enlevé status d'ici car il est mit par defaut 
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

#Fais avec IA car je ne savais pas comment faire
ItemImageFormSet = inlineformset_factory(
    Item, 
    ItemImage, 
    fields=['image'], 
    extra=5,      # Nombre de champs vides affichés
    max_num=5,    # Limite maximum de 5 photos[cite: 1]
    can_delete=False
)