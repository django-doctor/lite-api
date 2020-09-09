from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from api.search.application import documents


class ApplicationDocumentSerializer(DocumentSerializer):
    highlight = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        document = documents.ApplicationDocumentType
        fields = (
            "id",
            "reference_code",
            "case_type",
            "organisation",
            "status",
            "goods",
            "parties",
            "name",
            "destinations",
            "queues",
            "highlight",
        )

    def get_highlight(self, obj):
        if hasattr(obj.meta, 'highlight'):
            return obj.meta.highlight.to_dict()
        return {}

    def get_score(self, obj):
        return obj.meta.score
