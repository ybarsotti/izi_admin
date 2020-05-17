from django.db import models
from django.utils.translation import ugettext_lazy as _

from izi_admin.utils import DefaultDatesMixin, SoftDeleteMixin


def company_directory_path(instance, filename):
    return 'company_files/company_{0}/'.format(instance.id)


class Company(DefaultDatesMixin, SoftDeleteMixin, models.Model):
    user = models.ManyToManyField('users.User', related_name='user_company', blank=True)

    owner = models.ForeignKey('users.User', related_name='owner_company', blank=False, null=False,
                              on_delete=models.CASCADE)

    name = models.CharField(_('Nome da companhia'), max_length=128, default='Nova companhia')
    icon = models.ImageField(_('Imagem da companhia'), upload_to=company_directory_path, blank=True, null=True)

    class Meta:
        verbose_name = _('Companhia')
        verbose_name_plural = _('Companhias')

    def __str__(self):
        return self.name
