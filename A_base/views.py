from django.shortcuts import render

# Create your views here.


def test(request):
    template = "A_base/test.html"
    context = {}
    return render(request, template, context)
