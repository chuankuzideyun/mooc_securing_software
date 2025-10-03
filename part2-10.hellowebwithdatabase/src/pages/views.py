from django.http import HttpResponse
from .models import Message


# Create your views here.

def homePageView(request):
	m_id = request.GET.get('id')
	try:
		m = Message.objects.get(id = m_id)
		content = m.content
	except Message.DoesNotExist:
		content = "Message not found"

		
	return HttpResponse(content)
