from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from coreapp.api.serializers import ProfileSerializer, AddressSerializer
from coreapp.models import Address, User
from delivery.models import DeliveryRider, RiderDocuments, DeliveryRequest, OrderDelivery
from utility.models import GlobalSettings


class DocumentsSerializer(serializers.ModelSerializer):
    documents_url = serializers.CharField(source='get_documents_url', read_only=True)

    class Meta:
        model = RiderDocuments
        fields = ('title', 'documents', 'documents_url')


class DeliveryRiderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mobile', 'image')
        read_only_fields = ('email', 'mobile')


class DeliveryRiderProfileCreateSerializer(serializers.ModelSerializer):
    rider_documents = DocumentsSerializer(many=True, required=True)
    delivery_man = DeliveryRiderProfileSerializer(many=False, required=False)

    class Meta:
        model = DeliveryRider
        fields = ('address', 'rider_documents', 'vehicle_type', 'delivery_man')

    def create(self, validated_data):
        user = self.context['request'].user
        profile_data = validated_data.pop('delivery_man')
        rider_documents = validated_data.pop('rider_documents')
        for key, value in profile_data.items():
            setattr(user, key, value)
        user.save()
        delivery_rider = DeliveryRider.objects.create(**validated_data, delivery_man=user, account_balance=user.wallet)
        documents = [RiderDocuments.objects.create(**data) for data in rider_documents]
        delivery_rider.rider_documents.set(documents)
        return delivery_rider


class RiderProfileListSerializer(serializers.ModelSerializer):
    delivery_man = DeliveryRiderProfileSerializer(many=False, required=True)
    rider_documents = DocumentsSerializer(many=True, required=True)

    class Meta:
        model = DeliveryRider
        fields = ('delivery_man', 'address', 'rider_documents')


class DeliveryRequestAcceptOrRejectSerializer(serializers.Serializer):
    is_accepted = serializers.BooleanField()


class RiderDeliveryRequestListSerializer(serializers.ModelSerializer):
    pickup_point = serializers.SerializerMethodField()
    destination_address = serializers.SerializerMethodField()

    class Meta:
        model = DeliveryRequest
        fields = ('id', 'order', 'is_accepted', 'destination_address', 'pickup_point')

    def get_pickup_point(self, obj):
        return self.get_store_address()

    def get_store_address(self):
        global_settings = GlobalSettings.objects.first()
        store_address = {
            'address': global_settings.address,
            'latitude': float(global_settings.latitude),
            'longitude': float(global_settings.longitude),
        }
        return store_address

    def get_destination_address(self, obj):
        address = Address.objects.get(id=obj.order.shipping_address.id)
        destination_address = {
            'address': address.address,
            'country': address.country.name,
            'flat': address.flat,
            'road': address.road,
            'zip_code': address.zip_code,
            'latitude': float(address.latitude),
            'longitude': float(address.longitude),
        }
        return destination_address


class RiderOrderDeliverySerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(source='get_order_invoice', read_only=True)
    payment_status = serializers.CharField(source='get_payment_status', read_only=True)
    order_count = serializers.SerializerMethodField()

    class Meta:
        model = OrderDelivery
        fields = (
            'id', 'order', 'order_id', 'customer', 'order_count', 'payment_status', 'address', 'longitude', 'latitude',
            'rider'
        )

    def get_order_count(self, obj):
        filtered_orders = OrderDelivery.objects.filter(rider=obj.rider, status=obj.status)
        return filtered_orders.count()


class RiderStatusChangeSerializer(serializers.Serializer):
    rider_delivery_status = serializers.IntegerField(allow_null=False, required=True)


class RiderVerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(allow_blank=False, required=True)


class RiderLiverTrackSerializer(serializers.Serializer):
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, allow_null=False)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, allow_null=False)
