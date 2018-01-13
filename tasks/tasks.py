from celery import shared_task


@shared_task
def add(x ,y):
    print('Task add called with args: {}, {}'.format(x, y))
    return x + y

@shared_task
def mul(x ,y):
    print('Task mul called with args: {}, {}'.format(x, y))
    return x * y