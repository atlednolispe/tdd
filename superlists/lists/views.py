from django.shortcuts import (
    redirect, render)

from lists.models import Item, List


def home_page(request):
    # TODO 支持多个清单
    return render(request, 'home_page.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(
        request,
        'list.html',
        {'items': items})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % list_.id)
