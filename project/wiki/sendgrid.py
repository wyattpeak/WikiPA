from django.core.mail import send_mail

from .models import Request


def send_request_emails():
    requests = Request.objects.filter(state=Request.RequestState.REQUEST_RECEIVED)

    for request in requests:
        subject = 'Could you write this article'
        from_email = 'testsender@sausagemachine.net'
        recipient_list = [request.expert_email]

        message = f'''Hi {request.expert_name},

You've been asked to contribute your expertise on the h2otoday.sausagemachine.net wiki.

You were nominated as an expert on "{request.page_title}". If you could write a few paragraphs about it, it'd help us out a lot.

All you have to do is respond to this email with the content, followed by four tildes "~~~~", and it will automatically be added ot the wiki.

The requester added this message for you: {request.message}

Thanks very much for your help.
'''
        
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        request.state = Request.RequestState.EMAIL_SENT
        request.save()
