from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Pessoa
from .serializers import PessoaSerializer


class PessoaViewSet(GenericViewSet,  # generic view functionality
                    CreateModelMixin,  # handles POSTs
                    RetrieveModelMixin,  # handles GETs for 1 Company
                    UpdateModelMixin,  # handles PUTs and PATCHes
                    ListModelMixin):

    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

class PessoaEndpoint(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Pessoa.objects.get(pk=pk)
        except Pessoa.DoesNotExist:
            raise Http404

    def get(self, pk, format=None):
        Pessoa = self.get_object(pk)
        serializer = PessoaSerializer(Pessoa)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Pessoa = self.get_object(pk)
        serializer = PessoaSerializer(Pessoa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(PessoaSerializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk, format=None):
        Pessoa = self.get_object(pk)
        Pessoa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
