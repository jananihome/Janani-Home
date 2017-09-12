from django.shortcuts import render


def about_page(request):
    template = 'shared/about.html'
    return render(request, template, {})
