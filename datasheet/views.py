from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datasheet.forms import *
from datasheet.models import *

def index(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			basicForm = BasicForm(request.POST)
			explorationForm = ExplorationForm(request.POST)
			observedForm = ObservedForm(request.POST)
			weatherForm = WeatherForm(request.POST)
			countForm = CountForm(request.POST)
			if basicForm.is_valid() and explorationForm.is_valid() and observedForm.is_valid() and weatherForm.is_valid() and countForm.is_valid():
				basic = basicForm.save(commit = False)
				basic.createdBy = request.user
				basic.exploration_time = explorationForm.save()
				basic.butterflies_observed = observedForm.save()
				basic.weather = weatherForm.save()
				basic.count_time = countForm.save()
				basic.save()
				return redirect('next/?id='+str(basic.id))
			else:
				context = {"BasicForm": basicForm,"ExplorationForm":explorationForm,"ObservedForm":observedForm,"WeatherForm":weatherForm,"CountForm":countForm, }
				return render(request, "datasheet/index.html", context)
		else:
			basicForm = BasicForm()
			explorationForm = ExplorationForm()
			observedForm = ObservedForm()
			weatherForm = WeatherForm()
			countForm = CountForm()
			context = {"BasicForm": basicForm,"ExplorationForm":explorationForm,"ObservedForm":observedForm,"WeatherForm":weatherForm,"CountForm":countForm, }
		
			if "error" in request.session:
				context["error"] = request.session["error"]
				del request.session["error"]

			return render(request, "datasheet/index.html", context)
	else:
		return redirect("/accounts/")
		
def next(request):
	if request.method == 'GET' and 'id' in request.GET:
		id = request.GET['id']
		basic = Basic.objects.get(createdBy = request.user, id=id)
		clusters = ClusterInfo.objects.all().filter(basic = basic)
		clusterForm = ClusterForm()
		context = {'clusters':clusters,'ClusterForm': clusterForm,}
		return render(request, "datasheet/next.html", context)
	elif request.method == 'POST' and 'id' in request.GET:
		id = request.GET['id']
		basic = Basic.objects.get(createdBy = request.user, id=id)
		clusters = ClusterInfo.objects.all().filter(basic = basic)
		clusterForm = ClusterForm(request.POST)
		if clusterForm.is_valid():
			cluster = clusterForm.save(commit = False)
			cluster.basic = basic
			cluster.save()
			clusterForm = ClusterForm()
		context = {'clusters':clusters,'ClusterForm': clusterForm,}
		return render(request, "datasheet/next.html", context)		
	else:
		return HttpResponse("Didn't have id")