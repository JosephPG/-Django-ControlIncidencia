from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)

# Create your models here.


# Clase para el manejo de registro de usuario y usuario administrador
class CustomUsuarioManageDB(BaseUserManager):
    def create_user(self, usuario, password, nombre, ape_pat, ape_mat,
                    is_asesor):
        user = self.model(usuario=usuario, nombre=nombre, ape_pat=ape_pat,
                          ape_mat=ape_mat, is_asesor=is_asesor)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, password):
        user = self.create_user(usuario=usuario, password=password, nombre='',
                                ape_pat='', ape_mat='', is_asesor=True)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


# Modelo Usuario
class Usuario(AbstractBaseUser, PermissionsMixin):
    usuario = models.CharField(max_length=15, unique=True)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    nombre = models.CharField(max_length=40)
    ape_pat = models.CharField(max_length=30)
    ape_mat = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_asesor = models.BooleanField(default=False)

    USERNAME_FIELD = 'usuario'

    objects = CustomUsuarioManageDB()

    def get_full_name(self):
        return self.nombre + ' ' + self.ape_pat + ' ' + self.ape_mat

    def get_short_name(self):
        return self.usuario


# Modelo BackOffice
class BackOffice(models.Model):
    usuario = models.OneToOneField(Usuario, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.usuario.usuario)


# Modelo Asesor
class Asesor(models.Model):
    usuario = models.OneToOneField(Usuario, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.usuario.usuario)
