from django.shortcuts import render


#The welcome page
def welcome(request):
    return render(request, 'welcome.html')
