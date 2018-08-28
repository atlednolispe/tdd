from django.shortcuts import render

from lists.models import Item


def home_page(request):
    # TODO 每次请求产生空白记录
    # TODO 显示多个待办
    # TODO 支持多个清单
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
    else:
        new_item_text = ''

    return render(
        request,
        'home_page.html',
        {'new_item_text': new_item_text})

