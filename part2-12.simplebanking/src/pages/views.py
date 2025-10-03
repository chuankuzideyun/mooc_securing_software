from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account
from django.db.models import Q
import json



@login_required
def addView(request):
	if request.method == 'POST':
		iban = request.POST.get('iban')

		if not iban:
			try:
				data = json.loads(request.body.decode('utf-8'))
				iban = data.get('iban')
			except Exception:
				iban = None

		if not iban:
			return redirect('/')

		Account.objects.create(owner=request.user, iban=iban)
		return redirect('/')

	return redirect('/')

@login_required
def homePageView(request):
	#以下是自己的代码
	accounts = Account.objects.filter(owner=request.user).order_by('id')
	return render(request, 'pages/index.html', {'accounts': accounts})
