from rest_framework import serializers
from clothes.models import Brand, Size, Material, Color, Clothes

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

from rest_framework import serializers
from clothes.models import Brand, Size, Material, Color, Clothes

class ClothesSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    size = SizeSerializer()
    material = MaterialSerializer()
    color = ColorSerializer()

    class Meta:
        model = Clothes
        fields = '__all__'

    def create(self, validated_data):
        brand_data = validated_data.pop('brand')
        size_data = validated_data.pop('size')
        material_data = validated_data.pop('material')
        color_data = validated_data.pop('color')

        brand, _ = Brand.objects.get_or_create(name=brand_data['name'], defaults=brand_data)
        size, _ = Size.objects.get_or_create(size=size_data['size'], defaults=size_data)
        material, _ = Material.objects.get_or_create(type=material_data['type'], defaults=material_data)
        color, _ = Color.objects.get_or_create(name=color_data['name'], hex_code=color_data['hex_code'], defaults=color_data)

        clothes = Clothes.objects.create(
            brand=brand,
            size=size,
            material=material,
            color=color,
            **validated_data
        )
        return clothes

