from django.shortcuts import render


def index(request):
    return render(request, 'website/index.html', locals())

def contact(request):
    return render(request, 'website/contact.html', locals())


