from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Core'

    def ready(self):
        # On importe ici pour que Django ait fini de charger les modèles
        from .models import Category, Status, TradeType
        
        try:
            # Ici on crée les catégories avec pour le moment: Electronics, Furniture, Clothing, Books, Kitchen, Other
            for cat in ["Electronics", "Furniture", "Clothing", "Books", "Kitchen", "Other"]:
                Category.objects.get_or_create(title=cat)

            # Ici on crée les trade types (Selling, Giving away)
            for t in ["Selling", "Giving away"]:
                TradeType.objects.get_or_create(type=t)

            # Ici on crée les statuts
            for s in ["Available", "Sold"]:
                Status.objects.get_or_create(status=s)
        except:
            pass