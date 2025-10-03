import os

from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import File


@login_required
def deleteView(request):
	try:
		f = File.objects.get(pk=request.POST.get('id'), owner=request.user)
	except File.DoesNotExist:
		return redirect('/')
	f.delete()
	return redirect('/')


@login_required
def downloadView(request, fileid):
	try:
		f = File.objects.get(pk=fileid, owner=request.user)
	except File.DoesNotExist:
		return redirect('/')

	filename = os.path.basename(f.data.name)

	try:
		f.data.open('rb')
		data = f.data.read()
	finally:
		try:
			f.data.close()
		except Exception:
			pass

	response = HttpResponse(data, content_type='text/plain')
	response['Content-Disposition'] = f'attachment; filename="{filename}"'

	return response


@login_required
def addView(request):
	data = request.FILES.get('file')
	f = File(owner=request.user, data=data)
	f.save()
	return redirect('/')


@login_required
def homePageView(request):
	files = File.objects.filter(owner=request.user)
	uploads = [{'id': f.id, 'name': f.data.name.split('/')[-1]} for f in files]	
	return render(request, 'pages/index.html', {'uploads': uploads})
