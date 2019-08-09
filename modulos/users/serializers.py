from . models import Users, Municipio, Region
from rest_framework import serializers


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'email', 'password', 'id')


class MunicipioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Municipio
        fields = ('codigo', 'nombre', 'estado')


class ListMunicipioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Municipio
        fields = ('codigo', 'nombre', 'estado')


class RegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = ('codigo', 'nombre', 'municipios')


class ListRegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = ('codigo', 'nombre')
