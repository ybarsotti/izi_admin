from django.db import models
from django.utils.translation import ugettext_lazy as _

from izi_admin.utils import DefaultDatesMixin, SoftDeleteMixin


def team_directory_path(instance, filename):
    return 'team_files/team_{0}/'.format(instance.id)


class Team(DefaultDatesMixin, SoftDeleteMixin, models.Model):
    company = models.ForeignKey('companies.Company', related_name='team_company', on_delete=models.CASCADE)

    name = models.CharField(_('Nome do time'), default='New team', max_length=128)
    icon = models.ImageField(_('Imagem do time'), upload_to=team_directory_path, blank=True, null=True)

    class Meta:
        verbose_name = _('Time')
        verbose_name_plural = _('Times')

    def __str__(self):
        return self.name
