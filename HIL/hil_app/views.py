from django.shortcuts import render

from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from django.core.exceptions import FieldError

from .models import RSSUnsafe, Version, Frame, Clip

from django.http import HttpResponse, JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from rest_framework import status

from .serializers import RSSUnsafeModelSerializer, VersionMiniSerializer

from django.views.decorators.cache import cache_page
from django.core.cache import cache

import IPython


@api_view(['GET'])
def home(request):
    return Response('This works')


# @cache_page(60 * 5)
@api_view(['GET'])
def serve_rss(request):
    params = dict(request.query_params)
    print(params)
    if params:
        if 'version_name' in params:
            # IPython.embed()
            version_name = params['version_name'][0]
            version = Version.objects.get(version_name=version_name)
            rss_unsafe = RSSUnsafe.objects.filter(version=version)
        elif 'version_date' in params:
            version_date = params['version_date'][0]
            version = Version.objects.get(version_date__icontains=version_date)
            rss_unsafe = RSSUnsafe.objects.filter(version=version)
    else:
        rss_unsafe = RSSUnsafe.objects.all()

    res = RSSUnsafeModelSerializer(rss_unsafe, many=True)

    # versions_with_dates = Version.objects.values('version_name', 'version_date').distinct()

    # IPython.embed()
    return Response(res.data)


@api_view(['GET'])
def serve_rss_pagination(request):
    print('paginating')

    is_pagination = 'num' in request.query_params and 'size' in request.query_params

    params = dict(request.query_params)
    if is_pagination:
        params.pop('num')
        params.pop('size')
    all_rss_unsafe = RSSUnsafe.objects.all()

    filters = {}
    if params:
        valid_filters = ['pk', 'car_type', 'max_cost', 'year', 'min_year']

        frame_filters = ['ego_speed__gte', 'ego_speed__lte', 'yaw_rate__gte', 'yaw_rate__lte']
        clip_filters = ['time_of_day', 'weather', 'road_type', 'country', 'drive_name']
        version_filters = ['version_name', 'version_date', 'version_description']
        for k, v in params.items():
            # if k not in valid_filters:
            #     return Response({'status': 'error', 'info': f'{k} is not a valid filter!'}, status=status.HTTP_400_BAD_REQUEST)
            # filters[k] = float(v[0]) if v[0].isnumeric() else v[0]
            if k not in frame_filters + clip_filters + version_filters:
                if k != 'search':
                    filters[k] = v[0]
                else:
                    filters['trackfile__icontains'] = v[0]

        frame_filter_args = {}
        for frame_filter in frame_filters:
            if frame_filter in params:
                frame_filter_args[frame_filter] = params[frame_filter][0]
        filters['GFIStartFrame__in'] = Frame.objects.filter(**frame_filter_args)

        clip_filter_args = {}
        for clip_filter in clip_filters:
            if clip_filter in params:
                clip_filter_args[clip_filter] = params[clip_filter][0]
        filters['clip__in'] = Clip.objects.filter(**clip_filter_args)

        version_filter_args = {}
        for version_filter in version_filters:
            if version_filter in params:
                if version_filter == 'version_date':
                    ####### TO-DO: sync date format + sync date time zone ###############
                    # valid_date = params[version_filter][0].split()[0].replace('T', ' ')
                    # print('valid_date', valid_date)
                    # # IPython.embed()
                    # version_filter_args[version_filter] = parse_datetime(valid_date)
                    # print('date', parse_datetime(params[version_filter][0]))
                    print('#### PARAMS ####', params)
                    version_filter_args['version_date__icontains'] = params[version_filter][0].split('T')[0]
                else:
                    version_filter_args[version_filter] = params[version_filter][0]
        # IPython.embed()
        filters['version__in'] = Version.objects.filter(**version_filter_args)

        filtered_rss_unsafe = all_rss_unsafe.filter(**filters)

    else:
        filtered_rss_unsafe = all_rss_unsafe
    print('rss_unsafe', filtered_rss_unsafe)
    print('filters', filters)

    if is_pagination:
        page_num = int(request.query_params.get('num', 1)) - 1
        page_size = int(request.query_params.get('size', 10))

        start = page_num * page_size
        end = start + page_size

        # cache_data = cache.get(f'rss_{page_num}')
        # print(cache_data)
        # if cache_data:
        #     rss_data = cache_data
        #     print('FOUND CACHED DATA')
        # else:
        #     print('DID NOT FIND CACHED DATA')
        #     rss_unsafe = filtered_rss_unsafe[start:end]
        #     # total = Note.objects.count()
        #
        #     rss_data = RSSUnsafeModelSerializer(rss_unsafe, many=True).data
        #
        # cache.set(f'rss_{page_num}', rss_data)
        if filtered_rss_unsafe:
            rss_unsafe = filtered_rss_unsafe[start:end]
            rss_data = RSSUnsafeModelSerializer(rss_unsafe, many=True).data
        else:
            rss_data = []
        # IPython.embed()

        total = filtered_rss_unsafe.count()
        res = {'results': rss_data,
               'count': total,
               'has_more': end <= total,
               }
    else:
        if filtered_rss_unsafe:
            res = RSSUnsafeModelSerializer(filtered_rss_unsafe, many=True).data
        else:
            res = []

    return Response(res)


@api_view(['GET'])
def serve_versions(request):
    versions = Version.objects.all()
    res = VersionMiniSerializer(versions, many=True)
    # IPython.embed()
    return Response(res.data)

#
#
# @api_view(['GET'])
# def serve_notes_pagination(request):
#
#     page_num = int(request.query_params.get('num', 0))
#     page_size = int(request.query_params.get('size', 10))
#     start = page_num * page_size
#     end = start + page_size
#
#     notes = Note.objects.all()[start:end]
#     total = Note.objects.count()
#
#     notes_data = NoteModelSerializer(notes, many=True).data
#
#     res = {'data': notes_data,
#            'total': total,
#            'has_more': end <= total,
#            }
#
#     return Response(res)


@api_view(['POST'])
def signup(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")

        # new_user = User.objects.create_user(username=username, email=email, password=password)

        new_user = User()
        new_user.username = username
        new_user.email = email
        new_user.set_password(password)
        new_user.save()

        token = Token.objects.create(user=new_user)
        # IPython.embed()
        return Response({'token': str(token), 'status': 'ok', 'info': 'User created!'})

    except Exception as e:
        # IPython.embed()

        return Response({'status': 'error', 'info': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def validate_token(request):
    print(request.user.__dict__)
    return Response({'token-valid': True,
                     'username': request.user.username,
                     'first_name': request.user.first_name,
                     'last_name': request.user.last_name,
                     })


@api_view(['POST'])
# @authentication_classes([BasicAuthentication, TokenAuthentication])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_token(request):
    request.user.auth_token.delete()
    # token = Token.objects.get(user=request.user)
    # token.delete()
    return Response("OK")
