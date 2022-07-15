from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import CustomUser
from .permissions import IsAdmin
from .serializers import (CustomUserSerializer, SignUpSerializer,
                          TokenSerializer)
from api_yamdb import settings


class CustomUserViewSet(viewsets.ModelViewSet):
    """Вьюсет данных пользователей.
    Полный доступ к данным пользователей у администратора,
    чтение/изменение данных своей учетной записи юзером"""
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdmin, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username', )  # можно добавить связанную модель
    ordering_fields = 'username'
    ordering = 'username'
    lookup_field = 'username'
    lookup_url_kwarg = 'username'

    @action(methods=['get', 'patch', ], detail=False,
            permission_classes=(IsAuthenticated, ))
    def me(self, request):
        """Метод "me" отвечает за чтение и корректировку пользователем
        собственных учетных данных"""
        me_user = self.request.user
        serializer = self.get_serializer(me_user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(me_user, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=me_user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((AllowAny, ))
def get_confirmation_code(request):
    serializer = SignUpSerializer(data=request.data)
    username = serializer.initial_data.get('username')
    email = serializer.initial_data.get('email')
    if CustomUser.objects.filter(username=username,
                                 email=email).exists():
        user = CustomUser.objects.get(username=username,
                                      email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(subject='Confirmation code for yamdb',
                  message=f'Your confirmation code: {confirmation_code}. '
                          f'Your email: {user.email}. '
                          f'Your username: {user.username}.',
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[email],
                  )

    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        new_user = CustomUser.objects.create(username=username,
                                             email=email)
        confirmation_code = default_token_generator.make_token(new_user)
        send_mail(subject='Confirmation code for yamdb',
                  message=f'Your confirmation code: {confirmation_code}. '
                          f'Your email: {new_user.email}. '
                          f'Your username: {new_user.username}.',
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[email],
                  )
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes((AllowAny, ))
def get_token(request):
    """Метод "get_token" отвечает за получение зарегистрированным пользователем
    токена для доступа к сайту"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    new_user = get_object_or_404(CustomUser, username=username)

    if default_token_generator.check_token(new_user, confirmation_code):
        token = AccessToken.for_user(new_user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response({"confirmation_code": "Получен неверный confirmation_code"
                     }, status=status.HTTP_400_BAD_REQUEST)
