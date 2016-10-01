from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.http.response import HttpResponse
from golem.interfaces.facebook.interface import FacebookInterface
from .settings import FB_HUB_CHALLENGE,DIALOG_CONFIG
from .chatbot import get_new_settings
import json

class FacebookView(generic.View):

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == FB_HUB_CHALLENGE:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid hub challenge')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        if not FacebookInterface.message_queue:
            print('Initializing message queue...')
            FacebookInterface.init_queue(DIALOG_CONFIG)
            settings = get_new_settings()
            if settings:
                print('SENDING NEW SETTINGS')
                FacebookInterface.send_settings(settings)
        # Converts the text payload into a python dictionary
        request_body = json.loads(self.request.body.decode('utf-8'))
        FacebookInterface.accept_request(request_body)
        return HttpResponse()


