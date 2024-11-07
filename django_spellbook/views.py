from django.shortcuts import render


def view_introduction(request):
    return render(request, 'A_content/spellbook_md/introduction.html')
    

def view_djangolike(request):
    return render(request, 'A_content/spellbook_md/djangolike.html')
    

def view_spellbook_sb_intro(request):
    return render(request, 'A_content/spellbook_md/spellbook/sb_intro.html')
    