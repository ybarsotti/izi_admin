import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models

from izi_admin.utils import DefaultDatesMixin


def user_directory_path(instance, filename):
    return 'user_files/user_{0}/'.format(instance.id)


class UserManager(BaseUserManager):
    use_in_migrations = True

    @classmethod
    def normalize_email(cls, email):
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part
        return email.lower()

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Preencha com um email válido'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username = email
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if not password:
            raise ValueError("User must have a password")

        return self._create_user(email, password, **extra_fields)


class User(DefaultDatesMixin, AbstractUser):
    # Remover o campo username
    username = None

    USER_TYPE_CHOICES = (
        (('work'), _('Work')),
        (('student'), _('Student')),
    )

    favorite_projects = models.ManyToManyField('projects.Project', blank=True, verbose_name=_('Projetos favoritos'))

    email = models.EmailField(_('email'), max_length=256, unique=True,
                              error_messages={
                                  'unique': _("Já existe um usuario cadastrado com este email."),
                              })

    user_type = models.CharField(_('Tipo de usuário'), max_length=64, choices=USER_TYPE_CHOICES, null=False,
                                 blank=False)

    avatar = models.ImageField(_('Avatar'), blank=True, null=True, upload_to=user_directory_path)
    phone = models.CharField(_('Telefone'), max_length=18, blank=True, null=True)
    location = models.CharField(_('Localização'), max_length=256, blank=True, null=True)
    birthday = models.DateField(_('Data de aniversário'), blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
