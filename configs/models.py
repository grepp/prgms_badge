import datetime

from django.db import models


class BaseModelManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True).order_by('-updated_at')


class BaseModel(models.Model):
    objects = BaseModelManager()

    created_at = models.DateTimeField(
        verbose_name='추가된 일시',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='수정된 일시',
        auto_now=True
    )
    deleted_at = models.DateTimeField(
        verbose_name='삭제된 일시',
        blank=True,
        null=True,
        default=None
    )

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.datetime.now()
        self.save(update_fields=['deleted_at'])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])
