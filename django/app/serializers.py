from rest_framework import serializers


class NestingSerializer(serializers.Serializer):
    json_array = serializers.JSONField()
    keys_path = serializers.ListField(child=serializers.CharField())
