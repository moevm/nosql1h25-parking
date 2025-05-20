from .serializers import ParkingSerializer, UserSerializer, PaymentSerializer


def import_data(data: dict):
    for serializer_class in [
        ParkingSerializer,
        UserSerializer,
        PaymentSerializer
    ]:
        model = serializer_class.Meta.model
        db_table = model._meta.db_table

        ids = [item['id'] for item in data.get(db_table)]
        existing_objects = model.objects.filter(id__in=ids)
        existing_ids = [str(item.id) for item in existing_objects]
        non_existing_ids = set(ids) - set(existing_ids)
        non_existing_items = [
            item for item in data.get(db_table) if item['id'] in non_existing_ids
        ]

        create_serializer = serializer_class(
            many=True, data=non_existing_items
        )

        if create_serializer.is_valid():
            # model.objects.bulk_create(
            #     [model(**item) for item in create_serializer.validated_data]
            # )
            create_serializer.save()
        else:
            raise ValueError(
                f'Invalid data {db_table}'
            )

        items_to_update = {
            item['id']: item for item in data.get(db_table) if item['id'] in existing_ids
        }
        for existing_object in existing_objects:
            update_serializer = serializer_class(
                existing_object,
                data=items_to_update[str(existing_object.id)]
            )
            if update_serializer.is_valid():
                update_serializer.save()
                pass
            else:
                raise ValueError(
                    f'Invalid data {db_table}, pk={existing_object.id}'
                )
        #     for field_name, value in update_serializer.validated_data.items():
        #         setattr(existing_object, field_name, value)
        
        # fields = serializer_class().get_fields().keys()
        # fields = [field for field in fields if field != 'id'] 
        # model.objects.bulk_update(existing_objects, fields)
