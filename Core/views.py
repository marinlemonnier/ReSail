from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ItemForm, ItemImageFormSet, SignUpForm, EditProfileForm
from .models import Item, Status, Favorite
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm

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
            "error": "Invalid password or username"
        })
    return render(request, "registration/login.html")


#The welcome page
def welcome(request):
    items = Item.objects.all()
    query = request.GET.get('q')
    if query:
        items = items.filter(title__icontains=query)
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        items = items.order_by('price')
    elif sort_by == 'price_desc':
        items = items.order_by('-price')
    elif sort_by == 'title':
        items = items.order_by('title')
    else:
        items = items.order_by('-date_publication')
        
    user_favorite_ids = []
    if request.user.is_authenticated:
        # CORRECTION : On entoure la requête avec list() pour que le HTML puisse lire la liste proprement
        user_favorite_ids = list(Favorite.objects.filter(user=request.user).values_list('item_id', flat=True))
        
    return render(request, 'welcome.html', {
        'items': items,
        'user_favorite_ids': user_favorite_ids
    })

#Créer une annonce / on utilise ici @login_required pour vérifier que l'utilisateur est connecté avant de créer une annonce.
@login_required
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        formset = ItemImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            status_obj = Status.objects.get(status='Available')
            item.status = status_obj
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
    is_favorite = False
    # Ça récupère l'item spécifique grâce à l'ID passé dans l'URL
    item = get_object_or_404(Item, pk=item_id)
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, item=item).exists()
    
    return render(request, 'item_detail.html', {
        'item': item, 
        'is_favorite': is_favorite
        }) 
    

# Mon profil
def my_profile(request):
    user_items = request.user.item_set.all()
    return render(request, 'my_profile.html', {'user_items': user_items})

#Editer mon profil
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save() # Le formulaire gère la concaténation tout seul grâce à sa méthode save()
            return redirect('my_profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


#Supprimer umon annonce
@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if item.user == request.user:
        item.delete()
        return redirect('welcome')
    return redirect('item_detail', item_id=item_id)

#Modifier mon annonce
@login_required
def edit_item(request, item_id):
    # Récupération de l'item ou 404
    item = get_object_or_404(Item, pk=item_id)
    
    # Sécurité stricte : Seul le propriétaire peut modifier
    if item.user != request.user:
        return redirect('item_detail', item_id=item.id)
        
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        formset = ItemImageFormSet(request.POST, request.FILES, instance=item)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('item_detail', item_id=item.id)
    else:
        form = ItemForm(instance=item)
        formset = ItemImageFormSet(instance=item)
        
    return render(request, 'edit_item.html', {
        'form': form, 
        'formset': formset, 
        'item': item
    })

#Les favoris
@login_required
def favorites_list(request):
    """Affiche la page contenant uniquement les annonces enregistrées de l'utilisateur."""
    favorites = Favorite.objects.filter(user=request.user).select_related('item')
    return render(request, 'favorites.html', {'favorites': favorites})

@login_required
def toggle_favorite(request, item_id):
    """Ajoute ou retire une annonce des favoris puis redirige là où était l'utilisateur."""
    item = get_object_or_404(Item, pk=item_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, item=item)
    
    if not created:
        favorite.delete()
        
    # Redirige sur la page précédente (ou à l'accueil 'welcome' par défaut)
    return redirect(request.META.get('HTTP_REFERER', 'welcome'))