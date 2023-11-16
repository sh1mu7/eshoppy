from rest_framework.serializers import ModelSerializer
from delivery.models import DeliveryRider, RiderDocuments


class DocumentsSerializer(ModelSerializer):
    class Meta:
        model = RiderDocuments
        fields = ('title', 'documents')


class DeliveryRiderDocumentsSerializer(ModelSerializer):
    rider_documents = DocumentsSerializer(many=True)

    class Meta:
        model = DeliveryRider
        fields = ('vehicle_type', 'image', 'rider_documents')

    def create(self, validated_data):
        documents_data = validated_data.pop('rider_documents')
        user = self.context['request'].user
        delivery_rider = DeliveryRider.objects.create(delivery_man=user, account_balance=user.wallet, **validated_data)
        documents = []
        for data in documents_data:
            rider_document = RiderDocuments.objects.create(**data)
            documents.append(rider_document)
        delivery_rider.rider_documents.set(documents)
        return delivery_rider
