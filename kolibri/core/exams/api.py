from django.db.models.query import F
from django.shortcuts import get_object_or_404
from kolibri.auth.api import KolibriAuthPermissions, KolibriAuthPermissionsFilter
from kolibri.auth.filters import HierarchyRelationsFilter
from kolibri.core.exams import models, serializers
from rest_framework import filters, pagination, viewsets
from rest_framework.response import Response


class OptionalPageNumberPagination(pagination.PageNumberPagination):
    """
    Pagination class that allows for page number-style pagination, when requested.
    To activate, the `page_size` argument must be set. For example, to request the first 20 records:
    `?page_size=20&page=1`
    """
    page_size = None
    page_size_query_param = "page_size"

class ExamFilter(filters.FilterSet):

    class Meta:
        model = models.Exam
        fields = ['collection', ]

class ExamViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ExamSerializer
    pagination_class = OptionalPageNumberPagination
    permissions_classes = (KolibriAuthPermissions,)
    filter_backends = (KolibriAuthPermissionsFilter, filters.DjangoFilterBackend)
    filter_class = ExamFilter

    def get_queryset(self):
        return models.Exam.objects.all()


class ExamAssignmentViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ExamAssignmentSerializer
    pagination_class = OptionalPageNumberPagination
    permissions_classes = (KolibriAuthPermissions,)
    filter_backends = (KolibriAuthPermissionsFilter,)

    def get_queryset(self):
        return models.ExamAssignment.objects.all()


class UserExamViewset(viewsets.ModelViewSet):
    serializer_class = serializers.UserExamSerializer
    pagination_class = OptionalPageNumberPagination
    permissions_classes = (KolibriAuthPermissions,)
    filter_backends = (KolibriAuthPermissionsFilter,)

    def get_queryset(self):
        return models.ExamAssignment.objects.all()

    def retrieve(self, request, pk=None, **kwargs):
        exam = get_object_or_404(models.Exam.objects.all(), id=pk)
        assignment = HierarchyRelationsFilter(exam.assignments.get_queryset()).filter_by_hierarchy(
            target_user=request.user,
            ancestor_collection=F('collection'),
        ).first()
        serializer = serializers.UserExamSerializer(assignment, context={'request': request})
        return Response(serializer.data)
