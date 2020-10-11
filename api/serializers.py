from rest_framework import serializers
from api.models import User, Plotter, Template
from constans import USER_CLASS
from django.contrib.auth.models import Group


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
        group = Group.objects.get(name='user')
        user.groups.add(group)
        return user


class UserListSerializer(serializers.ModelSerializer):
    user_detail = serializers.CharField(source='get_user_url', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'email', 'user_detail']


class UserUserListSerializer(serializers.ModelSerializer):
    user_detail = serializers.CharField(source='get_user_user_url',
                                        read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'email', 'user_detail']


class DealerListSerializer(serializers.ModelSerializer):
    dealer_detail = serializers.CharField(source='get_dealer_url',
                                          read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'email', 'dealer_detail']


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
        group = Group.objects.get(name='dealer')
        user.groups.add(group)
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
        group = Group.objects.get(name='user')
        user.groups.add(group)
        return user


class PlotterAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plotter
        fields = ('user', 'format', 'count')


class PlotterDetailList(serializers.ModelSerializer):
    plotter_update = serializers.CharField(source='get_plotter_update',
                                           read_only=True)
    plotter_delete = serializers.CharField(source='get_plotter_delete',
                                           read_only=True)

    class Meta:
        model = Plotter
        fields = '__all__'


class TemplateAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('name', 'length', 'width', 'count')


class TemplateDetailList(serializers.ModelSerializer):
    template_change = serializers.CharField(source='get_template_change',
                                            read_only=True)

    class Meta:
        model = Template
        fields = '__all__'
