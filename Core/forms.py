from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Item, ItemImage, User
from django.forms import inlineformset_factory

PHONE_PREFIX_CHOICES = [('+33', '🇫🇷 +33'), ('+47', '🇳🇴 +47'), ('+44', '🇬🇧 +44'), ('+1', '🇺🇸 +1'), ('+46', '🇸🇪 +46'), ('+45', '🇩🇰 +45')]

class SignUpForm(UserCreationForm):
    phone_prefix = forms.ChoiceField(
        choices=PHONE_PREFIX_CHOICES, 
        widget=forms.Select(attrs={'class': 'phone-prefix-select'})
    )
    # On ajoute le champ manuellement pour qu'il soit traité par Django
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone_number", "profile_picture")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Application automatique des classes CSS à TOUS les champs
        for field in self.fields.values():
            if field.widget.input_type != 'file': # On ne touche pas au file input
                field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        prefix = self.cleaned_data.get('phone_prefix')
        number = self.cleaned_data.get('phone_number')
        user.phone_number = f"{prefix} {number}".strip()
        if commit:
            user.save()
        return user

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'currency', 'item_quality', 'country', 'city', 'neighborhood', 'trade_type', 'category']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

ItemImageFormSet = inlineformset_factory(
    Item, ItemImage, fields=['image'], extra=5, max_num=5, can_delete=False
)

class EditProfileForm(forms.ModelForm):
    phone_prefix = forms.ChoiceField(choices=PHONE_PREFIX_CHOICES, required=True, label="Préfixe")
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Logique de split pour l'édition
        if self.instance.pk and self.instance.phone_number:
            val = self.instance.phone_number
            for prefix, _ in PHONE_PREFIX_CHOICES:
                if val.startswith(prefix):
                    self.initial['phone_prefix'] = prefix
                    self.initial['phone_number'] = val.replace(prefix, '').strip()
                    break

    def save(self, commit=True):
        user = super().save(commit=False)
        prefix = self.cleaned_data.get('phone_prefix')
        number = self.cleaned_data.get('phone_number')
        user.phone_number = f"{prefix} {number}".strip()
        if commit:
            user.save()
        return user