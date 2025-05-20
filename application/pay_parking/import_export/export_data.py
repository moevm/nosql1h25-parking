from import_export.serializers import ParkingSerializer, UserSerializer, PaymentSerializer


def export_data():
    data = {}
    for serializer_class in [
        ParkingSerializer,
        UserSerializer,
        PaymentSerializer
    ]:
        model = serializer_class.Meta.model
        db_table = model._meta.db_table
        queryset = model.objects.all()
        data[db_table] = serializer_class(
            queryset, many=True
        ).data

    return data
