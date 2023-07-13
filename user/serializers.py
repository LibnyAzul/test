from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User

UserModel = get_user_model()


# La información que se mostrara al llamar la entidad con clave foranea
class UserFKSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name')


class PermissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename')


class GroupSerializers(serializers.ModelSerializer):
    permissions = PermissionSerializers(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'


# La información que se mostrara al llamar al objeto completo.
class UserSerializers(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    groups = GroupSerializers(many=True, read_only=True)

    @classmethod
    def get_token(self, user):
        token = RefreshToken.for_user(user)
        return str(token.access_token)

    class Meta:
        model = User
        fields = ('id', 'token', 'is_superuser', 'email', 'name', 'is_staff', 'alive', 'groups', 'user_permissions')
        lookup_fields = 'name'


# Información que se mostrara al listar el objeto.
class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'is_staff', 'is_superuser', 'groups', 'alive')


# Información que se mostrara al llamar el detalle del objeto
class UserDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class GroupSerializers(serializers.ModelSerializer):
    permissions = PermissionSerializers(many=True, read_only=True)
    class Meta:
        model = Group
        fields = '__all__'