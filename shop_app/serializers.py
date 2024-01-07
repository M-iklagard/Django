from rest_framework import serializers

class WarehouseSerializer(serializers.Serializer):
    warehouse = serializers.JSONField()