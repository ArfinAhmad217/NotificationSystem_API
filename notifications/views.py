from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import notify
from .models import Trigger, Template
from .serializers import TriggerSerializer, TemplateSerializer


@api_view(["POST"])
def fire_trigger(request, trigger_code):
    # Test recipients aa rahe hain request body se (real app me user session se aayenge)
    whatsapp_to = request.data.get("whatsapp_to")
    email_to = request.data.get("email_to")
    push_subscription_id = request.data.get("push_subscription_id")

    result = notify(
        trigger_code,
        whatsapp_to=whatsapp_to,
        email_to=email_to,
        push_subscription_id=push_subscription_id,
    )
    return Response(result)


@api_view(["GET"])
def list_triggers(request):
    triggers = Trigger.objects.all()
    return Response(TriggerSerializer(triggers, many=True).data)


@api_view(["GET"])
def list_templates(request):
    templates = Template.objects.all()
    return Response(TemplateSerializer(templates, many=True).data)
