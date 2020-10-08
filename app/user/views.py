from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from core.models import UserManager
from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    "create a new user in the system"
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    "create a new auth token for user"
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManagerUserView(generics.RetrieveUpdateAPIView):
    "manage the authenticated user"
    #queryset = UserManager.objects.filter(user=request.use)

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permissions_classes = (permissions.IsAuthenticated,)

    # def get_queryset(self):
    # return self.request.user

    def get_objects(self):
        "retrieve and return authenticated user"
        # queryset = UserManager.get_user()
        return self.request.user
