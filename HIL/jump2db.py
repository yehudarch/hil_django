import os
import django
import random
import string
import csv
import datetime

# import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HIL.settings")
django.setup()

from hil_app.models import RSSUnsafe, OnlineInterventions, Frame, Clip, Version
from hil_app.models import RSSUnsafeTemp

CSV_FILE = 'rss_safe_false_control_on_230725-234846_modified.jump'
CAUSE_OPTIONS = ['long_distance_spike', 'late_detection', 'drop_detection']
TOD_OPTIONS = ['day', 'night']
ROAD_OPTIONS = ['country', 'urban', 'highway']
WEATHER_OPTIONS = ['rain', 'clear', 'snow']
COUNTRY_OPTIONS = ['israel', 'usa']
VERSION_OPTIONS = ['version_1', 'version_2', 'version_3']
GFI_FIELDS = ['GFIStartFrame', 'GFIEndFrame']


def add_clips():
    with open(CSV_FILE, 'r') as fh:
        events = csv.DictReader(fh, delimiter=' ')
        all_clip_values = set(clip.clip for clip in Clip.objects.all())
        clip_data_instances = []
        for event in events:
            random_tod = random.choice(TOD_OPTIONS)
            random_road = random.choice(ROAD_OPTIONS)
            random_weather = random.choice(WEATHER_OPTIONS)
            random_country = random.choice(COUNTRY_OPTIONS)
            clip_value = event['clip']
            if clip_value not in all_clip_values:
                clip_data = Clip(
                    clip=clip_value,
                    drive_name=event['drive_name'],
                    time_of_day=random_tod,
                    weather=random_weather,
                    road_type=random_road,
                    country=random_country
                )
                clip_data_instances.append(clip_data)
                all_clip_values.add(clip_value)

        Clip.objects.bulk_create(clip_data_instances)


def add_frames():
    with open(CSV_FILE, 'r') as fh:
        events = csv.DictReader(fh, delimiter=' ')
        for event in events:
            for gfi_field in GFI_FIELDS:
                clip = Clip.objects.get(clip=event['clip'])
                gfi = event[gfi_field]

                # Check if a frame with the same clip and gfi combination already exists
                if not Frame.objects.filter(clip=clip, gfi=gfi).exists():
                    frame_data = Frame(
                        clip=clip,
                        gfi=gfi,
                        grab_index=event['grab_index'],
                        ego_speed=event['ego_speed'],
                        yaw_rate=event['yaw_rate'],
                    )
                    frame_data.save()


def add_versions():
    with open(CSV_FILE, 'r') as fh:
        # events = csv.DictReader(fh, delimiter=' ')
        version_instances = []
        for i, version_name in enumerate(VERSION_OPTIONS):
            version = Version(
                version_name=version_name,
                version_date=datetime.datetime.now() - datetime.timedelta(days=i),
                version_description=f'{version_name} {version_name} {i}{i+2}'
            )
            version_instances.append(version)

        Version.objects.bulk_create(version_instances)


def add_rssunsafe():
    with open(CSV_FILE, 'r') as fh:
        events = [x for x in csv.DictReader(fh, delimiter=' ')]
        rss_unsafe_instances = []
        for version_name in VERSION_OPTIONS:
            for event in events:
                # print(event)
                random_cause = random.choice(CAUSE_OPTIONS)
                clip_instance = Clip.objects.get(clip=event['clip'])
                # try:
                rss_unsafe = RSSUnsafe(
                    version=Version.objects.get(version_name=version_name),
                    trackfile=event['trackfile'],
                    clip=clip_instance,
                    object_id=event['id'],
                    GFIStartFrame=Frame.objects.get(clip=clip_instance, gfi=event['GFIStartFrame']),
                    GFIEndFrame=Frame.objects.get(clip=clip_instance, gfi=event['GFIEndFrame']),
                    root_cause=random_cause,
                    longitudinal_speed=event['longitudinal_speed'],
                    lateral_speed=event['lateral_speed'],
                    ego_motion_path_offset=event['ego_motion_path_offset'],
                    closest_by_ego_motion_path=event['closest_by_ego_motion_path'],
                    longitudinal_distance=event['longitudinal_distance'],
                    lateral_distance=event['lateral_distance'],
                    rss_safe=event['rss_safe'],
                    rss_longitudinal_score=event['rss_longitudinal_score'],
                    rss_lateral_score=event['rss_lateral_score'],
                    em_path_heading=event['em_path_heading'],
                    heading_vs_em_path=event['heading_vs_em_path'],
                    em_vt=event['em_vt'],
                    vt_towards_em_path=event['vt_towards_em_path'],
                    em_vm=event['em_vm'],
                    em_m=event['em_m'],
                    em_abs_t=event['em_abs_t'],
                    em_signed_t=event['em_signed_t'],
                    em_perc_of_seg=event['em_perc_of_seg'],
                    min_proj_dist_to_em_seg_edge=event['min_proj_dist_to_em_seg_edge'],
                    added_cutin_path=event['added_cutin_path'],
                    rss_lat_safe=event['rss_lat_safe'],
                    current_rss_lat_safe=event['current_rss_lat_safe'],
                    safe_lat_dist=event['safe_lat_dist'],
                    t_braking_dist_lat_brake=event['t_braking_dist_lat_brake'],
                    em_t_at_lateral_brake_lat=event['em_t_at_lateral_brake_lat'],
                    lat_brake_rss_lat_safe=event['lat_brake_rss_lat_safe'],
                    rss_lat_safe_lat_brake=event['rss_lat_safe_lat_brake'],
                    speed_based_heading=event['speed_based_heading'],
                    current_rss_lat_score=event['current_rss_lat_score'],
                    lat_brake_rss_lat_score=event['lat_brake_rss_lat_score'],
                    current_rss_lat_diff=event['current_rss_lat_diff'],
                    lat_brake_rss_lat_diff=event['lat_brake_rss_lat_diff'],
                    control_on=event['control_on'],

                )
                # except Frame.DoesNotExist:
                #     print(
                #     f"Frame matching query does not exist for clip {clip_instance.clip} and gfi {event['GFIEndFrame']}")
                #     continue  # Skip this iteration and proceed with the next event

                rss_unsafe.save()
            #     rss_unsafe_instances.append(rss_unsafe)
            #
            # RSSUnsafe.objects.bulk_create(rss_unsafe_instances)


def create_db_temp():
    with open(CSV_FILE, 'r') as fh:
        events = csv.DictReader(fh, delimiter=' ')
        rss_unsafe_instances = []
        for version_name in VERSION_OPTIONS:
            for event in events:
                # print(event)
                random_cause = random.choice(CAUSE_OPTIONS)
                rss_unsafe = RSSUnsafeTemp(
                    version_name=version_name,
                    trackfile=event['trackfile'],
                    clip=event['clip'],
                    object_id=event['id'],
                    GFIStartFrame=event['GFIStartFrame'],
                    GFIEndFrame=event['GFIEndFrame'],
                    root_cause=random_cause,
                    longitudinal_speed=event['longitudinal_speed'],
                    lateral_speed=event['lateral_speed'],
                    ego_motion_path_offset=event['ego_motion_path_offset'],
                    closest_by_ego_motion_path=event['closest_by_ego_motion_path'],
                    longitudinal_distance=event['longitudinal_distance'],
                    lateral_distance=event['lateral_distance'],
                    rss_safe=event['rss_safe'],
                    rss_longitudinal_score=event['rss_longitudinal_score'],
                    rss_lateral_score=event['rss_lateral_score'],
                    em_path_heading=event['em_path_heading'],
                    heading_vs_em_path=event['heading_vs_em_path'],
                    em_vt=event['em_vt'],
                    vt_towards_em_path=event['vt_towards_em_path'],
                    em_vm=event['em_vm'],
                    em_m=event['em_m'],
                    em_abs_t=event['em_abs_t'],
                    em_signed_t=event['em_signed_t'],
                    em_perc_of_seg=event['em_perc_of_seg'],
                    min_proj_dist_to_em_seg_edge=event['min_proj_dist_to_em_seg_edge'],
                    added_cutin_path=event['added_cutin_path'],
                    rss_lat_safe=event['rss_lat_safe'],
                    current_rss_lat_safe=event['current_rss_lat_safe'],
                    safe_lat_dist=event['safe_lat_dist'],
                    t_braking_dist_lat_brake=event['t_braking_dist_lat_brake'],
                    em_t_at_lateral_brake_lat=event['em_t_at_lateral_brake_lat'],
                    lat_brake_rss_lat_safe=event['lat_brake_rss_lat_safe'],
                    rss_lat_safe_lat_brake=event['rss_lat_safe_lat_brake'],
                    speed_based_heading=event['speed_based_heading'],
                    current_rss_lat_score=event['current_rss_lat_score'],
                    lat_brake_rss_lat_score=event['lat_brake_rss_lat_score'],
                    current_rss_lat_diff=event['current_rss_lat_diff'],
                    lat_brake_rss_lat_diff=event['lat_brake_rss_lat_diff'],
                    control_on=event['control_on'],

                )
                rss_unsafe_instances.append(rss_unsafe)

            RSSUnsafeTemp.objects.bulk_create(rss_unsafe_instances)


def update_clip():
    for clip in Clip.objects.all():
        clip.country = random.choice(COUNTRY_OPTIONS)
        clip.save()


if __name__ == "__main__":
    # create_db_temp()
    # add_clips()
    # add_frames()
    # add_versions()
    add_rssunsafe()
    # update_clip()

