from django.shortcuts import (
    redirect, render)

from lists.models import Item


def home_page(request):
    # TODO 支持多个清单
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()
    return render(
        request,
        'home_page.html',
        {'items': items})

