from pay_parking.filters import (
    ContainFilter, MinFilter, MaxFilter,
    BooleanExactFilter,
)


class FirstNameFiler(ContainFilter):
    parameter_name = 'first_name'
    field_name = 'first_name'


class SecondNameFiler(ContainFilter):
    parameter_name = 'second_name'
    field_name = 'second_name'


class ThirdNameFiler(ContainFilter):
    parameter_name = 'third_name'
    field_name = 'third_name'


class EmailFiler(ContainFilter):
    parameter_name = 'email'
    field_name = 'email'


class IsStaffFiler(BooleanExactFilter):
    parameter_name = 'is_staff'
    field_name = 'is_staff'


class MinLastLoginFiler(MinFilter):
    parameter_name = 'min_last_login'
    field_name = 'last_login'


class MaxLastLoginFiler(MaxFilter):
    parameter_name = 'max_last_login'
    field_name = 'last_login'


class MinCreatedAtFiler(MinFilter):
    parameter_name = 'min_created_at'
    field_name = 'created_at'


class MaxCreatedAtFiler(MaxFilter):
    parameter_name = 'max_created_at'
    field_name = 'created_at'


class MinUpdatedAtFiler(MinFilter):
    parameter_name = 'min_updated_at'
    field_name = 'updated_at'


class MaxUpdatedAtFiler(MaxFilter):
    parameter_name = 'max_updated_at'
    field_name = 'updated_at'
