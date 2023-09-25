from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Chat App")


def test(request):
    my_dict = {
        "insert_me": "This is a test", 
        "delete_me": "This is not a test"
        }
    return render(request, "chat/test.html", context=my_dict)