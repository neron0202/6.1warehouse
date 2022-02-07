from rest_framework import serializers
from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)       # настройте сериализатор для склада

    class Meta:
        model = Stock
        fields = ['address', 'positions']


    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
            StockProduct.objects.create(**position, stock=stock)
        return stock

        # достаем связанные данные для других таблиц
        # создаем склад по его параметрам

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions


    def create_or_update(defaults=None, **positions):
        defaults = {'price': positions['price'], 'quantity': positions['quantity']}
        try:
            obj = StockProduct.objects.get(stock=positions['stock'],  product=positions['product'])
            for key, value in defaults.items():
                setattr(obj, key, value)
        except StockProduct.DoesNotExist:
            new_values = {'price': positions['price'], 'quantity': positions['quantity']}
            new_values.update(defaults)
            obj = StockProduct(**new_values)
            obj.save()


        # obj, created = StockProduct.objects.update_or_create(product=positions['product'], defaults={'price': positions['price'], 'quantity': positions['quantity']})


    # def update(self, instance, validated_data):
    #     positions = validated_data.pop('positions')
    #     stock = super().update(instance, validated_data)
    #     for position in positions:
    #         StockProduct.objects.update(**position, stock=stock)
    #
    #     return stock

        # достаем связанные данные для других таблиц
        # обновляем склад по его параметрам

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions