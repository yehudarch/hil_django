from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='profile_images/')
    image_url = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name}, {self.last_name}"


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    screenshot_image = models.ImageField(upload_to='contact_images/')

    def __str__(self):
        return f"{self.user.username}, {self.title}"


class Clip(models.Model):
    clip = models.CharField(max_length=100, unique=True)
    drive_name = models.CharField(max_length=100)
    time_of_day = models.CharField(max_length=50)
    weather = models.CharField(max_length=50)
    road_type = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.clip}"


class Frame(models.Model):
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE)
    gfi = models.IntegerField()
    grab_index = models.IntegerField()
    ego_speed = models.FloatField()
    yaw_rate = models.FloatField()

    class Meta:
        unique_together = ('clip', 'gfi')

    def __str__(self):
        return f"Clip: {self.clip.clip}, 'gfi': {self.gfi}"


class OnlineInterventions(models.Model):
    # clip = models.ForeignKey(Frame, to_field='clip', on_delete=models.CASCADE)
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE)
    GFIStartFrame = models.ForeignKey(Frame, related_name='online_startframe', on_delete=models.CASCADE)
    GFIEndFrame = models.ForeignKey(Frame, related_name='online_endframe', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)


class Version(models.Model):
    version_name = models.CharField(max_length=50, unique=True)
    version_date = models.DateTimeField()
    # version_date = models.DateTimeField(auto_now_add=True)
    version_description = models.TextField(default='')

    def __str__(self):
        return f"version: {self.version_name}, Date: {self.version_date.strftime('%d-%m-%Y')}"


class RSSUnsafe(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    trackfile = models.CharField(max_length=100)
    # clip = models.ForeignKey(Frame, to_field='clip', on_delete=models.CASCADE)
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    GFIStartFrame = models.ForeignKey(Frame, related_name='rss_startframe', on_delete=models.CASCADE)
    GFIEndFrame = models.ForeignKey(Frame, related_name='rss_endframe', on_delete=models.CASCADE)
    root_cause = models.CharField(max_length=50)
    longitudinal_speed = models.FloatField()
    lateral_speed = models.FloatField()
    ego_motion_path_offset = models.FloatField()
    closest_by_ego_motion_path = models.BooleanField()
    longitudinal_distance = models.FloatField()
    lateral_distance = models.FloatField()
    rss_safe = models.BooleanField()
    rss_longitudinal_score = models.FloatField()
    rss_lateral_score = models.FloatField()
    em_path_heading = models.FloatField()
    heading_vs_em_path = models.FloatField()
    em_vt = models.FloatField()
    vt_towards_em_path = models.FloatField()
    em_vm = models.FloatField()
    em_m = models.FloatField()
    em_abs_t = models.FloatField()
    em_signed_t = models.FloatField()
    em_perc_of_seg = models.FloatField()
    min_proj_dist_to_em_seg_edge = models.FloatField()
    added_cutin_path = models.BooleanField()
    rss_lat_safe = models.BooleanField()
    current_rss_lat_safe = models.BooleanField()
    safe_lat_dist = models.FloatField()
    t_braking_dist_lat_brake = models.FloatField()
    em_t_at_lateral_brake_lat = models.FloatField()
    lat_brake_rss_lat_safe = models.BooleanField()
    rss_lat_safe_lat_brake = models.BooleanField()
    speed_based_heading = models.FloatField()
    current_rss_lat_score = models.FloatField()
    lat_brake_rss_lat_score = models.FloatField()
    current_rss_lat_diff = models.FloatField()
    lat_brake_rss_lat_diff = models.FloatField()
    control_on = models.FloatField()
    latitude = models.FloatField(null=True, default=None)
    longitude = models.FloatField(null=True, default=None)

    def __str__(self):
        return f"Clip: {self.clip.clip}, ID: {self.object_id}"


class RSSUnsafeTemp(models.Model):
    version_name = models.CharField(max_length=50)
    trackfile = models.CharField(max_length=50)
    clip = models.CharField(max_length=50)
    object_id = models.IntegerField()
    GFIStartFrame = models.IntegerField()
    GFIEndFrame = models.IntegerField()
    root_cause = models.CharField(max_length=50)
    longitudinal_speed = models.FloatField()
    lateral_speed = models.FloatField()
    ego_motion_path_offset = models.FloatField()
    closest_by_ego_motion_path = models.BooleanField()
    longitudinal_distance = models.FloatField()
    lateral_distance = models.FloatField()
    rss_safe = models.BooleanField()
    rss_longitudinal_score = models.FloatField()
    rss_lateral_score = models.FloatField()
    em_path_heading = models.FloatField()
    heading_vs_em_path = models.FloatField()
    em_vt = models.FloatField()
    vt_towards_em_path = models.FloatField()
    em_vm = models.FloatField()
    em_m = models.FloatField()
    em_abs_t = models.FloatField()
    em_signed_t = models.FloatField()
    em_perc_of_seg = models.FloatField()
    min_proj_dist_to_em_seg_edge = models.FloatField()
    added_cutin_path = models.BooleanField()
    rss_lat_safe = models.BooleanField()
    current_rss_lat_safe = models.BooleanField()
    safe_lat_dist = models.FloatField()
    t_braking_dist_lat_brake = models.FloatField()
    em_t_at_lateral_brake_lat = models.FloatField()
    lat_brake_rss_lat_safe = models.BooleanField()
    rss_lat_safe_lat_brake = models.BooleanField()
    speed_based_heading = models.FloatField()
    current_rss_lat_score = models.FloatField()
    lat_brake_rss_lat_score = models.FloatField()
    current_rss_lat_diff = models.FloatField()
    lat_brake_rss_lat_diff = models.FloatField()
    control_on = models.FloatField()

    def __str__(self):
        return f"Clip: {self.clip}, Opject_ID: {self.object_id}"
