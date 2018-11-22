#  rlcapp - record and organization management software for refugee law clinics
#  Copyright (C) 2018  Dominik Walser
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

from backend.recordmanagement import models, serializers
from backend.shared import storage_generator
from backend.static import error_codes, storage_folders


class RecordDocumentViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = models.RecordDocument.objects.all()
    serializer_class = serializers.RecordDocumentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        pass


class RecordDocumentUploadViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        """
        used to generate a presigned post, with that you can successfully upload a file to storage
        :param request:
        :param id:
        :return:
        """
        record = models.Record.objects.get(pk=id)
        if record is None:
            return Response(error_codes.ERROR__RECORD__RECORD__NOT_EXISTING)

        file_dir = storage_folders.get_storage_folder_record_document(record.from_rlc_id, record.id)
        file_name = request.query_params.get('file_name', '')
        file_type = request.query_params.get('file_type', '')

        return storage_generator.generate_presigned_post(file_name, file_type, file_dir)

    def post(self, request):
        pass


class RecordDocumentByRecordViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        pass

    def post(self, request, id):

        filename = request.data['filename']
        record = models.Record.objects.filter(pk=id).first()  # TODO: try catch?
        if not record:
            return Response(error_codes.ERROR__RECORD__RECORD__NOT_EXISTING, status=400)

        directory = storage_folders.get_storage_folder_record_document(record.from_rlc_id, record.id)
        information = storage_generator.check_file_and_get_information(directory, filename)
        if 'error' in information:
            return Response(information)

        already_existing = models.RecordDocument.objects.filter(name=information['key']).first()
        if already_existing is not None:
            already_existing.file_size = information['size']
            already_existing.last_edited = datetime.now()
            already_existing.save()

            serializer = serializers.RecordDocumentSerializer(already_existing)
            return Response(serializer.data)
        else:
            new_document = models.RecordDocument(record=record, name=information['key'], creator=request.user,
                                                 file_size=information['size'])
            new_document.save()

            serializer = serializers.RecordDocumentSerializer(new_document)
            return Response(serializer.data)
