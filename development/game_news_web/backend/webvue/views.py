from django.shortcuts import render

def vue_index(request):
    return render(request, 'vue_index.html')