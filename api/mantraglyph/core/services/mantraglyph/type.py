
import graphene
import django_filters
from .... import models as models
from query_optimizer import DjangoObjectType, filter


class MantraglyphFilter(filter.FilterSet):
    order_by = django_filters.OrderingFilter(
        fields=(
            [
                field.name + "__id" if field.is_relation else field.name
                for field in models.Mantraglyph._meta.fields
            ]
        )
    )

    class Meta:
        model = models.Mantraglyph
        fields = {
            field.name + "__id" if field.is_relation else field.name: ["exact"]
            for field in models.Mantraglyph._meta.fields
        }
        exclude = ["metadata"]         


class MantraglyphType(DjangoObjectType):

    class Meta:
        model = models.Mantraglyph
        filterset_class = MantraglyphFilter
        interfaces = (graphene.relay.Node,)
