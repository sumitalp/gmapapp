from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.template import loader
from .forms import UnitForm


def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('map_with_fusion_table/index.html')
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return HttpResponse(template.render(request))
