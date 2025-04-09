from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer, FullName, Address

class FullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullName
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    full_name = FullNameSerializer()
    address = AddressSerializer()
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'

    def update(self, instance, validated_data):
        full_name_data = validated_data.pop('full_name', {})
        address_data = validated_data.pop('address', {})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for attr, value in full_name_data.items():
            setattr(instance.full_name, attr, value)
        instance.full_name.save()

        for attr, value in address_data.items():
            setattr(instance.address, attr, value)
        instance.address.save()

        return instance

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    phone = serializers.CharField()
    full_name = FullNameSerializer()
    address = AddressSerializer()

    def create(self, validated_data):
        full_name_data = validated_data.pop('full_name')
        address_data = validated_data.pop('address')

        full_name = FullName.objects.create(**full_name_data)
        address = Address.objects.create(**address_data)

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        customer = Customer.objects.create(
            user=user,
            full_name=full_name,
            address=address,
            email=validated_data['email'],
            phone=validated_data['phone']
        )
        return customer
    
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        data['user'] = user
        return data

