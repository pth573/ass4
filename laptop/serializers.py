from rest_framework import serializers
from .models import Brand, Storage, Screen, GPU, Laptop

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'

class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = '__all__'

class GPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPU
        fields = '__all__'

class LaptopSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    storage = StorageSerializer()
    screen = ScreenSerializer()
    gpu = GPUSerializer()

    class Meta:
        model = Laptop
        fields = '__all__'

    def create(self, validated_data):
        brand_data = validated_data.pop('brand')
        storage_data = validated_data.pop('storage', None)
        screen_data = validated_data.pop('screen', None)
        gpu_data = validated_data.pop('gpu', None)

        brand, _ = Brand.objects.get_or_create(**brand_data)
        storage = Storage.objects.create(**storage_data) if storage_data else None
        screen = Screen.objects.create(**screen_data) if screen_data else None
        gpu = GPU.objects.create(**gpu_data) if gpu_data else None

        laptop = Laptop.objects.create(
            brand=brand, storage=storage, screen=screen, gpu=gpu, **validated_data
        )

        return laptop
