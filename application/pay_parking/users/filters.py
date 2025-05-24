from pay_parking.filters import (
    ContainFilter, MinFilter, MaxFilter,
    BooleanExactFilter,
)


class FirstNameFilter(ContainFilter):
    parameter_name = 'first_name'
    field_name = 'first_name'


class SecondNameFilter(ContainFilter):
    parameter_name = 'second_name'
    field_name = 'second_name'


class ThirdNameFilter(ContainFilter):
    parameter_name = 'third_name'
    field_name = 'third_name'


class EmailFilter(ContainFilter):
    parameter_name = 'email'
    field_name = 'email'


class IsStaffFilter(BooleanExactFilter):
    parameter_name = 'is_staff'
    field_name = 'is_staff'


class MinLastLoginFilter(MinFilter):
    parameter_name = 'min_last_login'
    field_name = 'last_login'


class MaxLastLoginFilter(MaxFilter):
    parameter_name = 'max_last_login'
    field_name = 'last_login'


class MinCreatedAtFilter(MinFilter):
    parameter_name = 'min_created_at'
    field_name = 'created_at'


class MaxCreatedAtFilter(MaxFilter):
    parameter_name = 'max_created_at'
    field_name = 'created_at'


class MinUpdatedAtFilter(MinFilter):
    parameter_name = 'min_updated_at'
    field_name = 'updated_at'


class MaxUpdatedAtFilter(MaxFilter):
    parameter_name = 'max_updated_at'
    field_name = 'updated_at'
