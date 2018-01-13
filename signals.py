from django.db.models.signals import post_save
from django.dispatch import receiver

from client.models import Job
import cluster_tasks


@receiver(post_save, sender=Job)
def start_job(sender, instance, created, **kwargs):
    print('signal start')
    try:
        task = getattr(cluster_tasks, instance.task.name)
    except AttributeError:
        raise Exception('Incorrect task name')
    else:
        task.delay(**instance.kwargs)
