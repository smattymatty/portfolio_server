from django.shortcuts import render


def view_test(request):
    return render(request, 'test_content/spellbook_md/test.html')
    

def view_folder1_test1(request):
    return render(request, 'test_content/spellbook_md/folder1/test1.html')
    

def view_folder2_test2(request):
    return render(request, 'test_content/spellbook_md/folder2/test2.html')
    