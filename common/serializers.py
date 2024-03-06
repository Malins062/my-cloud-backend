from rest_framework import serializers


class IntegerFieldAsString(serializers.Field):
    def to_internal_value(self, data):
        try:
            return int(data)
        except ValueError:
            self.fail('invalid')
