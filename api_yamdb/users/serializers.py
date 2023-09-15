from rest_framework import serializers

from .models import User
from .validators import validate_pattern_symbols, max_length, max_length254
from rest_framework.validators import UniqueValidator

class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Выберите другое имя пользователя'
            )
        return value

    class Meta:
        model = User
        fields = ['email', 'username']


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all()), validate_pattern_symbols, max_length],
        required=True,
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all()), max_length254]
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']
