from .models import Logo

def logo(request):
    return {'footer_log': Logo.objects.get(title='logo')}
