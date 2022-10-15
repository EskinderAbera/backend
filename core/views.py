from django.contrib.auth import login
from django.http import JsonResponse
from rest_framework import generics, mixins, status, permissions
from rest_framework.response import Response
from core.models import *
from .serializers import *
from rest_framework.views import APIView

# Create your views here.

class CreateMessage(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = SenderMessage.objects.all()
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        res = self.create(request, *args, **kwargs)
        if res.status_code == 201:
            return Response({'msg': 'successfully created'}, status=status.HTTP_201_CREATED)


class ActiveHospital(APIView):

    def get(self, request, format = None):
        drivers = Driver.objects.filter(isactive = True)
        Hospitales = []
        for driver in drivers:
            hospital = Hospital.objects.get(id = driver.hospital.id)
            serializer = HospitalSerializer(hospital)
            Hospitales.append(serializer.data)
        return Response(Hospitales, status=status.HTTP_200_OK)



class HospitalMessageView(APIView):
    def get(self, request, pk, format = None):
        try:
            message = SenderMessage.objects.filter(hospital = pk)
        except:
            return Response({"msg" : "No message is found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(message, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format = None):
        serializer = LoginSerializer(data=request.data, context = {'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        profile = Profile.objects.get(user = user)
        if profile.role.rolename == 'hospitaluser':
            messages = SenderMessage.objects.filter(hospital = profile.hospital, isactive = True)
            activedrivers = Driver.objects.filter(hospital = profile.hospital, isactive = True)
            drivers = Driver.objects.filter(hospital = profile.hospital)
            messageserializer = MessageSerializer(messages, many = True)
            activedriverserialized = DriveSerializer(activedrivers, many=True)
            driverserialized = DriveSerializer(drivers, many = True)
            res = []
            res.append({"messages": messageserializer.data})
            res.append({"activedrivers": activedriverserialized.data})
            res.append({"drivers": driverserialized.data})
            return Response(res, status=status.HTTP_200_OK)
        else:
            messages = profile.user_message.filter(isactive = True)
            serializer = MessageSerializer(messages, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        


