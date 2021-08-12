from rest_framework import serializers
from .models import Recollection


# Сериализаторы подобны формам в Django
class RecollectionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Recollection
		fields = ('id', 'name', 'description', 'user', 'geom')