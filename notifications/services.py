import requests
from decouple import config


# ---------- WhatsApp via Twilio Sandbox ----------
def send_whatsapp(to_number, message_body):
    account_sid = config("TWILIO_ACCOUNT_SID")
    auth_token = config("TWILIO_AUTH_TOKEN")
    from_number = config("TWILIO_WHATSAPP_FROM")  # e.g. whatsapp:+17372508034

    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    to_whatsapp = to_number if to_number.startswith("whatsapp:") else f"whatsapp:+{to_number.lstrip('+')}"

    payload = {
        "To": to_whatsapp,
        "From": from_number,
        "Body": message_body,
    }
    resp = requests.post(url, data=payload, auth=(account_sid, auth_token))
    return resp.status_code, resp.text


# ---------- Email via Brevo (free tier, simple REST) ----------
def send_email(to_email, subject, body):
    api_key = config("BREVO_API_KEY")
    from_email = config("BREVO_FROM_EMAIL")
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "sender": {"email": from_email},
        "to": [{"email": to_email}],
        "subject": subject or "Notification",
        "htmlContent": f"<p>{body}</p>",
    }
    resp = requests.post(url, headers=headers, json=payload)
    return resp.status_code, resp.text


# ---------- Web Push via OneSignal ----------
def send_web_push(subscription_id, title, body):
    app_id = config("ONESIGNAL_APP_ID")
    api_key = config("ONESIGNAL_REST_API_KEY")
    url = "https://onesignal.com/api/v1/notifications"
    headers = {
        "Authorization": f"Basic {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "app_id": app_id,
        "include_subscription_ids": [subscription_id],
        "headings": {"en": title},
        "contents": {"en": body},
    }
    resp = requests.post(url, headers=headers, json=payload)
    return resp.status_code, resp.text


# ---------- Master notify function ----------
def notify(trigger_code, *, whatsapp_to=None, email_to=None, push_subscription_id=None):
    from .models import Trigger

    results = {}
    try:
        trigger = Trigger.objects.get(code=trigger_code)
    except Trigger.DoesNotExist:
        return {"error": f"No trigger with code '{trigger_code}'"}

    for template in trigger.templates.filter(is_active=True):
        if template.channel == "whatsapp" and whatsapp_to:
            results["whatsapp"] = send_whatsapp(whatsapp_to, template.body)
        elif template.channel == "email" and email_to:
            results["email"] = send_email(email_to, template.subject, template.body)
        elif template.channel == "web_push" and push_subscription_id:
            results["web_push"] = send_web_push(push_subscription_id, template.subject or trigger.name, template.body)

    return results