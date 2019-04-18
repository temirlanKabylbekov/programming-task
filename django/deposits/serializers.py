from rest_framework import serializers

from deposits.models import Deposit


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ('id', 'city', 'country', 'currency', 'amount')
        extra_kwargs = {field: {'required': False} for field in fields if field != 'id'}


class DepositNestingSerializer(serializers.Serializer):
    keys_path = serializers.ListField(child=serializers.CharField())
