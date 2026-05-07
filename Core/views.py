from django.shortcuts import render, redirect, get_object_or_404
from .forms import ItemForm, ItemImageFormSet, SignUpForm
from .models import Item
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

def logout_view(request):
    logout(request) # Déconnecte l'utilisateur
    return redirect('welcome') # Redirige vers la page d'accueil 

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('welcome')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')
        return render(request, "registration/login.html", {
            "username": username, 
            "error": "Identifiants invalides"
        })
    return render(request, "registration/login.html")


#The welcome page
def welcome(request):
    items = Item.objects.all()  # Récupère tous les objets pour les afficher sur la page d'accueil
    return render(request, 'welcome.html', {'items': items})

#Créer une annonce / on utilise ici @login_required pour vérifier que l'utilisateur est connecté avant de créer une annonce.
@login_required
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        formset = ItemImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            formset.instance = item
            formset.save()
            return render(request, 'item_success.html', {'item': item})
    else:
        form = ItemForm()
        formset = ItemImageFormSet()
    return render(request, 'create_item.html', {'form': form, 'formset': formset})


# Tout le detail de l'annonce
def item_detail(request, item_id):
    # Ça récupère l'item spécifique grâce à l'ID passé dans l'URL
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'item_detail.html', {'item': item}) 
    