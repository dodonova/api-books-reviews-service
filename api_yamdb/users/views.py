from django.core.mail import send_mail
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from .models import User
from django.shortcuts import get_object_or_404
from .serializers import RegistrationSerializer, UserSerializer, TokenSerializer
from django.http import Http404, HttpResponse
from http.client import BAD_REQUEST, OK
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdmin

from .httpmethod import HTTPMethod

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="Регистрация на YamDB",
        message=f"Код для токена: {confirmation_code}",
        from_email='fromexample@mail.ru',
        recipient_list=[user.email],
    )
    return Response(serializer.data, status = OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def token_jwt(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=OK)

    return Response(serializer.errors, status=BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['username', ]
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    @action(detail=False,
            methods=[HTTPMethod.GET.value, HTTPMethod.PATCH.value, ],
            permission_classes=[permissions.IsAuthenticated, ])
    def me(self, request):
        serializer = UserSerializer(request.user,
                                    data=request.data,
                                    partial=True)
        if request.user.role == 'admin' or request.user.role == 'moderator':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=OK)
        serializer.is_valid(raise_exception=True)
        serializer.save(role='user')
        return Response(serializer.data, status=OK)
