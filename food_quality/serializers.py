from rest_framework import serializers

class PredictionSerializer(serializers.Serializer):
    features = serializers.ListField(
        child=serializers.FloatField(),
        allow_empty=False
    )
