from django.shortcuts import render, redirect, get_object_or_404
from .forms import ItemForm, ItemImageFormSet, SignUpForm
from .models import Item, Status
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
    return render(request, 'welcome.html', {'items': items})

#Ancien version crash test 
#def welcome(request):
    #items = Item.objects.all().order_by('-date_publication')  # Récupère tous les objets pour les afficher sur la page d'accueil dans l'ordre d'ajout 
    #return render(request, 'welcome.html', {'items': items})

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
    # Ça récupère l'item spécifique grâce à l'ID passé dans l'URL
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'item_detail.html', {'item': item}) 
    

# Mon profil
def my_profile(request):
    return render(request, 'my_profile.html')

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