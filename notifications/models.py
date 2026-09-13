from django.db import models


class Trigger(models.Model):
    code = models.CharField(max_length=50, unique=True)  # e.g. "login", "logout"
    name = models.CharField(max_length=100)               # e.g. "Login"

    def __str__(self):
        return self.name


class Template(models.Model):
    CHANNEL_CHOICES = [
        ("whatsapp", "WhatsApp"),
        ("email", "Email"),
        ("web_push", "Web Push"),
    ]

    trigger = models.ForeignKey(Trigger, related_name="templates", on_delete=models.CASCADE)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    subject = models.CharField(max_length=200, blank=True)   # email only
    body = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("trigger", "channel")

    def __str__(self):
        return f"{self.trigger.name} - {self.channel}"
