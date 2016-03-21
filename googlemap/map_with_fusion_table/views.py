from urllib.request import urlopen
from io import StringIO, BytesIO
from PIL import Image
from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.template import loader
from .forms import UnitForm
from map_with_fusion_table.models import Unit


def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('map_with_fusion_table/index.html')
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    if request.method == "POST":
        lat = request.POST.get('lat', 0)
        lng = request.POST.get('lng', 0)

        if not is_water(lat, lng):
            form = UnitForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse(Unit.objects.all())
    return HttpResponse(template.render(request))

def validate_latlng(request, *args, **kwargs):
    if request.method == "POST":
        lat = request.POST.get('lat', 0)
        lng = request.POST.get('lng', 0)

        #if not is_water(lat, lng)

    return HttpResponse(True)

def is_water(lat, lng):
    web_sock = urlopen("http://maps.googleapis.com/maps/api/staticmap?"
                     "scale=2&center="+str(lat)+","+str(lng)+"&zoom=13&size=20x20&sensor=false&visual_refresh=true"
                     "&style=element:labels|visibility:off&style=feature:water|color:0x00FF00"
                     "&style=feature:transit|visibility:off&style=feature:poi|visibility:off"
                     "&style=feature:road|visibility:off&style=feature:administrative|visibility:off")

    imgdata = BytesIO(web_sock.read())

    im = Image.open(imgdata)
    rgb_im = im.convert('RGB')
    r, g, b = rgb_im.getpixel((0, 0))

    print (r, g, b)
    # pix = im.load()
    # print(im.size) #Get the width and hight of the image for iterating over
    # print(pix[0,0]) #Get the RGBA Value of the a pixel of an image
    # pix[x,y] = value # Set the RGBA Value of the image (tuple)
    if g == 254:
        return True
    return False
