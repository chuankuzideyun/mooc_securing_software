from django.shortcuts import render

def homePageView(request):
	items = request.session.get('items', [])
	return render(request, 'pages/index.html', {'items': items})

def addPageView(request):
	items = request.session.get('items', [])

	if request.method == "POST":
		content = request.POST.get("content", "").strip()
		if content:
			items.insert(0, content)       # add newest first
			items = items[:10]             # keep only 10 most recent
			request.session['items'] = items

	return render(request, 'pages/index.html', {'items': items})

def erasePageView(request):
	request.session['items'] = []
	return render(request, 'pages/index.html', {'items': []})
