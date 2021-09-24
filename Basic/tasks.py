from celery import shared_task
from celery.utils.log import get_task_logger

# from django.apps import apps

from diluprod21.celery import app

from .models import taskTracker


logger = get_task_logger(__name__)


@app.task(bind=True,)
def import_data_task(self, data_resource, dataset):
    logger.info(f"crear instancia de taskTracker con tarea {self.__name__}")
    instance = get_task_tracker_instance(self.request.id, self.__name__)

    logger.info(f"ejecutar tarea {self.__name__}")
    try:
        import_data(data_resource, dataset)
    except Exception as exc:
        instance.status = 'FAILED'
        instance.type_error = exc
        instance.save()
        raise self.retry(exc=exc, max_retries=3, countdown=20)

    logger.info("actualizar instancia de taskTracker")
    instance.status = 'FINISHED'
    instance.save()

    # print('Executing task id {0.id}, args: {0.args} kwargs: {0.kwargs}'.format(
    #     self.request))
    logger.info("tarea finalizada")


def get_task_tracker_instance(id, task_name):
    instance, new = taskTracker.objects.get_or_create(
        task=task_name,
        defaults={'task_id': id,
                  'status': 'WORKING',
                  'type_error': None}
    )

    if not new:
        instance.task_id = id
        instance.status = 'WORKING'
        instance.type_error = None
        instance.save()
    return instance


def import_data(data_resource, dataset):
    # data_resource = apps.get_model('Basic.{}'.format(data_resource_name)) #cargar modelo solo con el nombre

    result = data_resource.import_data(
        dataset, dry_run=True,raise_errors=True)  # Test the data import
    if result.has_errors():
        raise ValueError("error al cargar el archivo")
    else:
        data_resource.import_data(
            dataset, dry_run=False)  # Actually import now
