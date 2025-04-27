# announcements/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Announcement
from users.models import CustomUser as User


@receiver(post_save, sender=Announcement)
def notify_users_on_announcement(sender, instance, created, **kwargs):
    if not created:
        return

    subject = f"Νέα ανακοίνωση: {instance.title}"
    message = instance.content

    recipients = User.objects.filter(is_active=True)
    if instance.type == 'manager':
        recipients = recipients.filter(is_staff=False, role='tenant')
    elif instance.type == 'internal':
        recipients = recipients.filter(is_staff=False, role='internal_admin')

    emails = recipients.values_list('email', flat=True)

    if emails:
        send_mail(
            subject,
            message,
            'noreply@oikodomiko.gr',
            list(emails),
            fail_silently=True
        )


