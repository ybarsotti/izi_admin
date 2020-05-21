from django.db import models
from django.utils.translation import ugettext_lazy as _

from izi_admin.utils import DefaultDatesMixin, SoftDeleteMixin


class Column(DefaultDatesMixin, SoftDeleteMixin, models.Model):
    name = models.CharField(_('Nome da coluna'), max_length=64, null=False, blank=False, default=_('Backlog'))

    class Meta:
        verbose_name = _('Coluna')
        verbose_name_plural = _('Colunas')

    def __str__(self):
        return self.name


class Project(DefaultDatesMixin, SoftDeleteMixin, models.Model):
    team = models.ManyToManyField('teams.Team', verbose_name=_('Times'))
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, verbose_name=_('Companhia'))
    column = models.ManyToManyField('Column', verbose_name=_('Colunas'))

    name = models.CharField(_('Nome do projeto'), max_length=64, null=False, blank=False)
    image = models.ImageField(_('Imagem do projeto'), upload_to='project_images/', blank=True, null=True)

    class Meta:
        verbose_name = _('Projeto')
        verbose_name_plural = _('Projetos')
        ordering = ['name', ]

    def __str__(self):
        return self.name


class Sprint(DefaultDatesMixin, SoftDeleteMixin, models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name=_('Projeto'))
    name = models.CharField(_('Nome'), blank=False, null=False, max_length=64, default='Sprint')
    description = models.CharField(_('Descrição'), max_length=256, null=True, blank=True)
    start_date = models.DateField(_('Data de início'))
    finish_date = models.DateField(_('Data de término'), blank=True, null=True)

    class Meta:
        verbose_name = _('Sprint')
        verbose_name_plural = _('Sprints')
        ordering = ['project']

    def __str__(self):
        return self.name