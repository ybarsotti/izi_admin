from django.db import models

from django.utils.translation import ugettext_lazy as _

from izi_admin.utils import SoftDeleteMixin, DefaultDatesMixin


class Card(DefaultDatesMixin, SoftDeleteMixin, models.Model):
    PRIORITY_CHOICES = [
        ('Baixa', _('Baixa')),
        ('Média', _('Média')),
        ('Alta', _('Alta')),
        ('Urgente', _('Urgente')),
    ]

    title = models.CharField(_('Título'), max_length=64, null=False, blank=False)
    description = models.CharField(_('Descrição'), max_length=512, blank=True, null=True)
    column = models.ForeignKey('projects.Column', on_delete=models.CASCADE, verbose_name=_('Coluna'), null=True,
                               blank=True, related_name='card_column')
    creator = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name=_('Criador'),
                                related_name='card_creator')
    responsible = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name=_('Responsável'),
                                    related_name='card_responsible')
    priority = models.CharField(_('Prioridade'), max_length=128, null=False, blank=False, choices=PRIORITY_CHOICES,
                                default=PRIORITY_CHOICES[1])
    sprint = models.ForeignKey('projects.Sprint', on_delete=models.CASCADE, verbose_name=_('Sprint'),
                               related_name='card_sprint')
    estimated_time = models.DecimalField(_('Tempo estimado'), decimal_places=2, max_digits=4)
    work_time = models.DecimalField(_('Tempo trabalhado'), decimal_places=2, max_digits=4)

    class Meta:
        verbose_name = _('Card')
        verbose_name_plural = _('Cards')

    def __str__(self):
        return self.title