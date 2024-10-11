from django.shortcuts import render
from django.core.mail import send_mail
from store_mgmnt import settings

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        subject = request.POST['topic']
        email = request.POST['email']
        message = request.POST['message']
        # Construct the full message to include the sender's details
        full_message = f"Message from {name} ({email}):\n\n{message}"
        try: 
            send_mail(
                subject,
                full_message,
                settings.EMAIL_HOST_USER,
                ['ehab.youssiff@gmail.com'],  # Replace with your recipient email address
            )
            return render(request, 'thank.html', {'name': name})
        except Exception as e:
            print(f'Error sending email: {e}')
        
    return render(request, 'contact.html', {})


