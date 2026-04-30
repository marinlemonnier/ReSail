from django.shortcuts import render, redirect, get_object_or_404
from .forms import ItemForm
from .models import Item


#The welcome page
def welcome(request):
    items = Item.objects.all()  # Récupère tous les objets pour les afficher sur la page d'accueil
    return render(request, 'welcome.html', {'items': items})

#Créer une annonce
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user  # Associe l'annonce à l'utilisateur connecté
            item.save()
            return render(request, 'item_success.html', {'item': item})
    else:
        form = ItemForm()
    return render(request, 'create_item.html', {'form': form})

# Tout le detail de l'annonce
def item_detail(request, item_id):
    # Ça récupère l'item spécifique grâce à l'ID passé dans l'URL
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'item_detail.html', {'item': item}) 
    