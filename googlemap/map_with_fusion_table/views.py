import os
from urllib.request import urlopen
from io import StringIO, BytesIO
from PIL import Image
import httplib2
from googleapiclient.discovery import build
import oauth2client
from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials
from oauth2client.file import Storage
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from django.http import HttpResponse
from django.template import loader
from oauth2client.tools import argparser
from .forms import UnitForm
from map_with_fusion_table.models import Unit


SCOPES = 'https://www.googleapis.com/auth/fusiontables'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Fusion Table API'

def index(request, *args, **kwargs):
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

    # Here's the file you get from API Console -> Service Account.

    # Create an httplib2.Http object to handle our HTTP requests and authorize it
      # with the Credentials. Note that the first parameter, service_account_name,
      # is the Email address created for the Service account. It must be the email
      # address associated with the key that was created.
    # credentials = AppAssertionCredentials(
    #     # 'shepany@amsas-staging.iam.gserviceaccount.com',
    #     # key,
    #     scope='https://www.googleapis.com/auth/fusiontables')

    # credentials = oauth2callback()
    # http = httplib2.Http()
    # http = credentials.authorize(http)

    # flow = flow_from_clientsecrets(file_path, scope='https://www.googleapis.com/auth/fusiontables')
    # flow.params['include_granted_scopes'] = True
    # print(flow)
    # service = build("fusiontables", "v1", http=http)
    # For example, let make SQL query to SELECT ALL from Table with
    # id = 1gvB3SedL89vG5r1128nUN5ICyyw7Wio5g1w1mbk
    # print(service.query().sql(sql='SELECT * FROM 1rVH53DHk3t13HbLlUfGlQLBWYy7X25WABYJfeVmJ').execute())
    kw = {
        'request': request
    }
    if 'credentials' not in request.session:
        return redirect(reverse('maps:oauth2callback'))

    credentials = OAuth2Credentials.from_json(request.session['credentials'])
    if credentials.access_token_expired:
        return redirect(reverse('maps:oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        service = build('fusiontables', 'v1', http=http_auth)
        print(service.query().sql(sql='SELECT * FROM 1rVH53DHk3t13HbLlUfGlQLBWYy7X25WABYJfeVmJ').execute())

    print(request.session.get('credentials'))

    return HttpResponse(template.render(request))

def oauth2callback(request, *args, **kwargs):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    file_path = os.path.dirname(os.path.dirname(__file__))
    # if not os.path.exists(credential_dir):
    #     os.makedirs(credential_dir)
    # credential_path = os.path.join(credential_dir,
    #                                'ft-python-quickstart.json')
    # 
    # store = Storage(credential_path)
    # credentials = store.get()
    # 
    # if not credentials or credentials.invalid:
    #     flow = flow_from_clientsecrets(os.path.join(file_path, CLIENT_SECRET_FILE), SCOPES,
    #                                    redirect_uri='http://localhost:8080/map/oauth2callback/')
    #     flow.user_agent = APPLICATION_NAME
    #     # auth_uri = flow.step1_get_authorize_url()
    #     # redirect(auth_uri)
    #     credentials = tools.run_flow(flow, store, argparser.parse_args([]))
    #     print('Storing credentials to ' + credential_path)
    flow = flow_from_clientsecrets(
          os.path.join(file_path, CLIENT_SECRET_FILE),
          SCOPES,
          redirect_uri=request.build_absolute_uri(reverse('maps:oauth2callback')),
    )
    code = request.GET.get('code', None)
    if code is None:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        # auth_code = request.get('code')
        credentials = flow.step2_exchange(code)
        request.session['credentials'] = credentials.to_json()
        return redirect(reverse('maps:index'))


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
