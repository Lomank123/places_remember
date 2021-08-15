from rest_framework import serializers

from coreapp.models import Recollection


class RecollectionSerializer(serializers.ModelSerializer):


	class Meta:
		model = Recollection
		fields = ('id', 'name', 'description', 'user', 'geom')