from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from api.tasks.scrap_m3 import ScrapperM3
from api.models import Property 
from api.serializers import PropertySerializer

from rest_framework import permissions


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def seed(request):
    if request.method == "POST":
        limit = request.query_params.get("limit")
        if limit is not None:
            scrapper = ScrapperM3('https://inmuebles.metroscubicos.com/propiedades-individuales/', int(limit))
            try:
                scrapper.run()
            except:
                print("Something wrong happened :(")
            return HttpResponse(status=200)
        else: 
            return HttpResponse(status=400)

@api_view(["GET"])
@permission_classes((permissions.AllowAny,))

def properties_list(request):
    """
    List all properties
    """
    limit = request.query_params.get("limit")
    if limit is not None:
        properties = Property.objects.order_by('-id')[:int(limit)]
        serializer = PropertySerializer(reversed(properties), many=True)
        return JsonResponse(serializer.data, safe=False)
    else: 
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return JsonResponse(serializer.data, safe=False)