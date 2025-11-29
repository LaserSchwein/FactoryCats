from django.shortcuts import render

def home_page(request):
    return render(request, 'anton.html')  # ваш HTML файл
