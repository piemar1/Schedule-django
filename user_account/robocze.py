from django.core.mail import send_mail

subject = "SandboxApp: Confirm registration"


text = "Hi , \n please confirm Your registration by clicking or copy-past this link \n" \
       "/accounts/activate/%s/ \n Please confirm with in 48 houers. Thank You for using our app." \
       " \n Your Sandbox Team"

send_mail(subject, text, 'pieczka1@wp.pl', ['marcin-pieczynski@wp.pl'], fail_silently=False)
