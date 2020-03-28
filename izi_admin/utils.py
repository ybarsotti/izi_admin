import uuid

from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone


class SoftDeleteQuerySet(QuerySet):
    """
    Efetua os soft deletes dos campos relacionados ao model
    """
    def delete(self):
        for obj in self:
            obj.deleted_at = timezone.now()
            obj.save()

    def undelete(self):
        for obj in self:
            obj.deleted_at = None
            obj.save()


class SoftDeleteManager(models.Manager):
    """
    Mostra apenas os dados que NÃO foram "deletados" (deleted_at = None)
    """

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)


class DefaultDatesMixin(models.Model):
    """
    Modelo base para a maioria das models, fornecendo 'criado_em', 'atualizado_em' e 'id' no formato UUID (Versão 4)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """
    Modelo base para soft deletes (deleted_at)
    """
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    objects = SoftDeleteManager()
    original_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def undelete(self):
        self.deleted_at = None
        self.save()
