from rest_framework import authentication, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.nest import NestValidationError, nester
from deposits.models import Deposit
from deposits.serializers import DepositNestingSerializer, DepositSerializer


class DepositViewSet(viewsets.ModelViewSet):
    queryset = Deposit.objects.all().order_by('id')
    serializer_class = DepositSerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def nest(self, request):
        serializer = DepositNestingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = nester(Deposit.objects.values(), serializer.validated_data['keys_path'])
            return Response(result)
        except NestValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
