from rest_framework import serializers
from mobile.models import Brand, Screen, Battery, Camera, Storage, Mobile

class BrandMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = '__all__'

class BatterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Battery
        fields = '__all__'

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'

class MobileSerializer(serializers.ModelSerializer):
    brand = BrandMobileSerializer()
    screen = ScreenSerializer()
    battery = BatterySerializer()
    camera = CameraSerializer()
    storage = StorageSerializer()

    class Meta:
        model = Mobile
        fields = '__all__'  # Sửa từ '_all_' thành '__all__'

    def create(self, validated_data):
        brand_data = validated_data.pop('brand')
        screen_data = validated_data.pop('screen', None)
        battery_data = validated_data.pop('battery', None)
        camera_data = validated_data.pop('camera', None)
        storage_data = validated_data.pop('storage', None)

        brand, _ = Brand.objects.get_or_create(**brand_data)  # Sửa `MobileBrand` thành `Brand`
        screen = Screen.objects.get_or_create(**screen_data)[0] if screen_data else None
        battery = Battery.objects.get_or_create(**battery_data)[0] if battery_data else None
        camera = Camera.objects.get_or_create(**camera_data)[0] if camera_data else None
        storage = Storage.objects.get_or_create(**storage_data)[0] if storage_data else None

        mobile = Mobile.objects.create(
            brand=brand,
            screen=screen,
            battery=battery,
            camera=camera,
            storage=storage,
            **validated_data  # Đảm bảo các trường khác cũng được lưu
        )

        return mobile
