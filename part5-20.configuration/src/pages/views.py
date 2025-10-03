from Demos.win32ts_logoff_disconnected import username
from django.contrib.messages.context_processors import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.models import User
from django.db import transaction
from django.views.decorators.http import require_POST

from .models import Account


@login_required
@csrf_protect
@require_POST
def transferView(request):
	
	if request.method == 'GET':
		to = User.objects.get(username=request.GET.get('to'))
		amount = int(request.GET.get('amount'))

	if not to or not amount:
		return redirect('/')
	try:
		if amount < 0:
			return redirect('/')
	except ValueError:
		messages.error(request, "Invalid amount.")
		return redirect('/')

	to_user = get_object_or_404(User, username=to)

	if request.user.balance >= amount:
		request.user.balance -= amount
		to_user.balance += amount
		request.user.save()
		to_user.save()
	
	return redirect('/')



@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts})
