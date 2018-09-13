""" rlcapp - record and organization management software for refugee law clinics
Copyright (C) 2018  Dominik Walser

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/> """
from rest_framework import serializers
from ..models import Record
from .tag import TagNameSerializer


class RecordFullDetailSerializer(serializers.ModelSerializer):
    tagged = TagNameSerializer(many=True, read_only=True)

    class Meta:
        model = Record
        fields = '__all__'
        extra_kwargs = {
            'creator': {
                'read_only': True
            }
        }
    # TODO: create Record, validate Data?


class RecordNoDetailSerializer(serializers.ModelSerializer):
    tagged = TagNameSerializer(many=True, read_only=True)
    state = serializers.CharField()

    class Meta:
        model = Record
        fields = ('id', 'created_on', 'state',
                  'record_token', 'working_on_record', 'tagged')


# TODO: anonymized records?? old records, but well researched
