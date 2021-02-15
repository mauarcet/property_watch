from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from api.tasks.scrap_m3 import ScrapperM3
from api.models import Property 


@csrf_exempt
def seed(request):
    if request.method == "POST":
        scrapper = ScrapperM3('https://inmuebles.metroscubicos.com/propiedades-individuales/', 10)
        try:
            scrapper.run()
        except:
            print("Something wrong happened :(")
        return HttpResponse(status=200)

