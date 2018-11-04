from moneyed import Money
from educational_need.models import EducationalNeed
from rest_framework import serializers


class MoneyField(serializers.Field):
    def to_representation(self, obj):
        return {
            'amount': "%f" % (obj.amount),
            'currency': "%s" % (obj.currency),
        }
    def to_internal_value(self, data):
        return Money(data['amount'], data['currency'])


class EducationalNeedSerializer(serializers.HyperlinkedModelSerializer):
    amount_required = MoneyField()
    class Meta:
        model = EducationalNeed
        exclude = ()
