from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task, TaskHistory

@receiver(pre_save, sender=Task)
def track_task_changes(sender, instance, **kwargs):
    if instance.pk:  # Только для существующих задач
        old_task = Task.objects.get(pk=instance.pk)
        changes = {}
        for field in ['title', 'description', 'date', 'is_completed']:
            old_value = getattr(old_task, field)
            new_value = getattr(instance, field)
            if old_value != new_value:
                changes[field] = {
                    "old": str(old_value),
                    "new": str(new_value)
                }
        if changes:
            TaskHistory.objects.create(
                task=instance,
                user=instance.user,
                changes=changes
            )