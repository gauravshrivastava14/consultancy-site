from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Service, Technology
from .forms import ContactForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')


def home(request):
    services = Service.objects.all()
    technologies = Technology.objects.all()
    
    context = {
        'services': services,
        'technologies': technologies,
    }
    return render(request, 'home.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact_request = form.save(commit=False)
            contact_request.ip_address = request.META.get('REMOTE_ADDR')
            contact_request.save()
            
            # Send email notification
            send_mail(
                subject=f"New Contact Request from {contact_request.name}",
                message=f"""
                Name: {contact_request.name}
                Email: {contact_request.email}
                Company: {contact_request.company or 'Not provided'}
                Phone: {contact_request.phone or 'Not provided'}
                
                Message:
                {contact_request.message}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=True,
            )
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

class ServiceListView(ListView):
    model = Service
    template_name = 'services.html'
    context_object_name = 'services'

class TechnologyListView(ListView):
    model = Technology
    template_name = 'technologies.html'
    context_object_name = 'technologies'