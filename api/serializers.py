from rest_framework import serializers
from api.models import User, Plotter, Template
from constans import USER_CLASS


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'email', ]


class UserDetailList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserDealerCreate(UserRegisterSerializer):
    """Create Dealer by administrator."""
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],

        )
        user.set_password(validated_data['password'])
        user.class_user = USER_CLASS['Dealer']
        user.save()
        return user


class UserUserCreate(UserRegisterSerializer):
    """Create User by Dealer."""
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
        )
        user.set_password(validated_data['password'])
        user.dealer_id = self.context['request'].user.id
        user.save()
        return user


class PlotterAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plotter
        fields = ('user', 'format', 'count')


class PlotterDetailList(serializers.ModelSerializer):
    class Meta:
        model = Plotter
        fields = '__all__'


class TemplateAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('name', 'length', 'width', 'count')


class TemplateDetailList(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'
