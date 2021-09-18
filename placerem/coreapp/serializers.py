from rest_framework import serializers

from coreapp.models import Recollection, CustomUser


class RecollectionSerializer(serializers.ModelSerializer):


	class Meta:
		model = Recollection
		fields = ('id', 'name', 'description', 'user', 'geom')


class CustomUserSerializer(serializers.ModelSerializer):


	class Meta:
		model = CustomUser
		fields = ('id', 'email', 'username')