from django.contrib.auth.models import User
from rest_framework import serializers
from record.models import Bill, Category, Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()

    class Meta:
        model = Category
        fields = '__all__'


class BillSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    group = serializers.StringRelatedField()

    class Meta:
        model = Bill
        fields = '__all__'
