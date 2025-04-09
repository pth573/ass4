# from rest_framework import serializers
# from .models import FullName, Address, Customer

# class FullNameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FullName
#         fields = '__all__' 

# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         fields = '__all__'


# class CustomerSerializer(serializers.ModelSerializer):
#     full_name = serializers.PrimaryKeyRelatedField(queryset=FullName.objects.all(), write_only=True)
#     address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), write_only=True)

#     class Meta:
#         model = Customer
#         fields = '__all__'

#     def create(self, validated_data):
#         full_name_data = validated_data.pop('full_name')
#         address_data = validated_data.pop('address')

#         full_name = FullName.objects.create(**full_name_data)
#         address = Address.objects.create(**address_data)

#         customer = Customer.objects.create(full_name=full_name, address=address, **validated_data)
#         return customer

#     def update(self, instance, validated_data):
#         full_name_data = validated_data.pop('full_name', None)
#         address_data = validated_data.pop('address', None)

#         if full_name_data:
#             for attr, value in full_name_data.items():
#                 setattr(instance.full_name, attr, value)
#             instance.full_name.save()

#         if address_data:
#             for attr, value in address_data.items():
#                 setattr(instance.address, attr, value)
#             instance.address.save()

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()
#         return instance



from rest_framework import serializers
from .models import FullName, Address, Customer

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

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        full_name_data = validated_data.pop('full_name')
        address_data = validated_data.pop('address')

        full_name = FullName.objects.create(**full_name_data)
        address = Address.objects.create(**address_data)

        customer = Customer.objects.create(full_name=full_name, address=address, **validated_data)
        return customer

    def update(self, instance, validated_data):
        full_name_data = validated_data.pop('full_name', None)
        address_data = validated_data.pop('address', None)

        if full_name_data:
            for attr, value in full_name_data.items():
                setattr(instance.full_name, attr, value)
            instance.full_name.save()

        if address_data:
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)
            instance.address.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
