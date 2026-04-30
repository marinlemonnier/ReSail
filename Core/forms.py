from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        # On liste les champs que l'utilisateur doit remplir
        fields = [
            'title', 'description', 'price', 'currency', 
            'item_quality', 'country', 'city', 'neighborhood', 
            'trade_type', 'status', 'category'
        ]


