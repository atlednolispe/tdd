from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    if request.method == 'POST':
        return render(
            request,
            'home_page.html',
            {'new_item_text': request.POST['item_text']})
    return render(request, 'home_page.html')
