from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework import permissions


class UserManager(BaseUserManager):
    def create(self, name, email, password, createdBy):
        if not email:
            raise ValueError('User must have an Email address')

        if not name:
            raise ValueError('User must have a Username')

        if not password:
            raise ValueError('User must have a Password')

        email = self.normalize_email(email)

        lastModifiedBy = createdBy
        if createdBy is None:
            createdBy = 'System'
            lastModifiedBy = 'System'

        user = self.model(
            name=name,
            email=email,
            createdBy=createdBy,
            lastModifiedBy=lastModifiedBy,
            alive=True)
        user.set_password(password)
        user.save()
        return user

    def update(self, id, name, email, password, lastModifiedBy):
        if not email:
            raise ValueError('User must have an Email address')

        if not name:
            raise ValueError('User must have a Username')

        if not password:
            raise ValueError('User must have a Password')

        user = self.model.get(pk=id)
        user.email = self.normalize_email(email)
        if password:
            user.set_password(password)

        if not lastModifiedBy:
            user.lastModifiedBy = lastModifiedBy
        else:
            user.lastModifiedBy = 'System'

        user.save()
        return user

    def create_superuser(self, email, name, password):
        user = self.create(name, email, password, 'System')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=20, unique=True)
    fullName = models.CharField(max_length=255)
    email = models.CharField(max_length=50, unique=True)
    cellPhone = models.CharField(max_length=15)
    birthdate = models.CharField(max_length=10)
    is_staff = models.BooleanField(default=False)
    alive = models.BooleanField(default=True)
    createdBy = models.CharField(max_length=254)
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedBy = models.CharField(max_length=254)
    lastModifiedDate = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']