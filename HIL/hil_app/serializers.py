from rest_framework import serializers
from .models import RSSUnsafe, Frame, Clip, Version


class VersionMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Version
        fields = '__all__'


class FrameMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Frame
        fields = ("gfi", "grab_index",)


class RSSUnsafeModelSerializer(serializers.ModelSerializer):
    # GFIStartFrame = FrameMiniSerializer(read_only=True)
    # GFIEndFrame = FrameMiniSerializer(read_only=True)
    trackfile = serializers.CharField()
    object_id = serializers.IntegerField()
    root_cause = serializers.CharField()
    gfi_startframe = serializers.IntegerField(source='GFIStartFrame.gfi')
    gfi_endframe = serializers.IntegerField(source='GFIEndFrame.gfi')
    gi_startframe = serializers.IntegerField(source='GFIStartFrame.grab_index')
    gi_endframe = serializers.IntegerField(source='GFIEndFrame.grab_index')
    ego_speed = serializers.FloatField(source='GFIStartFrame.ego_speed')
    yaw_rate = serializers.FloatField(source='GFIStartFrame.yaw_rate')

    time_of_day = serializers.CharField(source='clip.time_of_day')
    weather = serializers.CharField(source='clip.weather')
    road_type = serializers.CharField(source='clip.road_type')
    country = serializers.CharField(source='clip.country')
    drive_name = serializers.CharField(source='clip.drive_name')

    version_name = serializers.CharField(source='version.version_name')
    version_date = serializers.DateTimeField(source='version.version_date')
    version_description = serializers.CharField(source='version.version_description')

    class Meta:
        model = RSSUnsafe
        # fields = '__all__'
        exclude = ['id', 'GFIStartFrame', 'GFIEndFrame', 'clip', 'version']
        # extra_fields = [
        #     'gfi_startframe',
        #     'gi_startframe',
        #     'gfi_endframe',
        #     'gi_endframe',
        #     'ego_speed',
        #     'yaw_rate'
        # ]



class RSSUnsafeSerializer(serializers.Serializer):
    GFIStartFrame = FrameMiniSerializer(read_only=True)
    GFIEndFrame = FrameMiniSerializer(read_only=True)

    # def create(self, validated_data):
    #     return RSSUnsafe.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.save()
    #     return instance


