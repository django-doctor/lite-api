from rest_framework import serializers, relations

from end_user.models import EndUser
from organisations.models import Organisation


class EndUserCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    address = serializers.CharField()
    country = serializers.CharField()
    website = serializers.URLField(required=False, allow_blank=True)
    type = serializers.ChoiceField(choices=EndUser.END_USER_TYPE)
    organisation = relations.PrimaryKeyRelatedField(queryset=Organisation.objects.all())

    class Meta:
        model = EndUser
        fields = ('id',
                  'name',
                  'address',
                  'country',
                  'website',
                  'type',
                  'organisation')


class EndUserViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = EndUser
        fields = ('id',
                  'name',
                  'address',
                  'country',
                  'website',
                  'type',
                  'organisation')


class EndUserUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = EndUser
        fields = ('id',
                  'name',
                  'address',
                  'country',
                  'website',
                  'type',
                  'organisation')

    def update(self, instance, validated_data):
        """
        Update and return an existing `Site` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.country = validated_data.get('country', instance.country)
        instance.website = validated_data.get('website', instance.website)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance