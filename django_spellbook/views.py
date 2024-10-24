from django.shortcuts import render


def view_test(request):
    return render(request, 'A_content/spellbook_md/test.html')
    

def view_folder_1_test_span(request):
    return render(request, 'A_content/spellbook_md/folder_1/test_span.html')
    

def view_folder_1_test_1(request):
    return render(request, 'A_content/spellbook_md/folder_1/test_1.html')
    

def view_folder_1_subfolder1_hey(request):
    return render(request, 'A_content/spellbook_md/folder_1/subfolder1/hey.html')
    

def view_spells_my_spells(request):
    return render(request, 'A_content/spellbook_md/spells/my_spells.html')
    