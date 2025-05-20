from paying.models import Payment
from parking.models import Parking, EmbeddedParking
from users.models import EmbeddedUser, User
from rest_framework import serializers


class ParkingSerializer(serializers.ModelSerializer):
    id = serializers.CharField(min_length=24, max_length=24)

    class Meta:
        model = Parking
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(min_length=24, max_length=24)

    class Meta:
        model = User
        fields = '__all__'


class EmbeddedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmbeddedUser
        exclude = ('id', )


class EmbeddedParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmbeddedParking
        exclude = ('id', )


class PaymentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(min_length=24, max_length=24)
    parking_id = serializers.CharField(min_length=24, max_length=24)
    user_id = serializers.CharField(min_length=24, max_length=24)
    parking_detail = EmbeddedParkingSerializer()
    user_detail = EmbeddedUserSerializer()

    class Meta:
        model = Payment
        exclude = ('parking', 'user')
