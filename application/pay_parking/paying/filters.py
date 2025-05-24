from pay_parking.filters import (
    ContainFilter, ExactFilter, MinFilter, MaxFilter,
    MaxHourDurationFilter, MinHourDurationFilter, BooleanExactFilter,
    IntergerExactFilter
)


class MinCreatedAtFilter(MinFilter):
    parameter_name = 'min_created_at'
    field_name = 'created_at'


class MaxCreatedAtFilter(MaxFilter):
    parameter_name = 'max_created_at'
    field_name = 'created_at'


class MinStartFilter(MinFilter):
    parameter_name = 'min_start'
    field_name = 'start'


class MaxStartFilter(MaxFilter):
    parameter_name = 'max_start'
    field_name = 'end'


class MinEndFilter(MinFilter):
    parameter_name = 'min_end'
    field_name = 'end'


class MaxEndFilter(MaxFilter):
    parameter_name = 'max_end'
    field_name = 'end'


class MinPriceFilter(MinFilter):
    parameter_name = 'min_price'
    field_name = 'price'


class MaxPriceFilter(MaxFilter):
    parameter_name = 'max_price'
    field_name = 'price'


class MinDurationFilter(MinHourDurationFilter):
    parameter_name = 'min_duration'
    field_name = 'duration'


class MaxDurationFilter(MaxHourDurationFilter):
    parameter_name = 'max_duration'
    field_name = 'duration'


class AddressFilter(ContainFilter):
    parameter_name = 'address'
    field_name = 'parking_detail__address'


class ParkingZoneFilter(IntergerExactFilter):
    parameter_name = 'parking_zone'
    field_name = 'parking_detail__parking_zone'


class MinLatitudeFilter(MinFilter):
    parameter_name = 'min_latitude'
    field_name = 'parking_detail__latitude'


class MaxLatitudeFilter(MaxFilter):
    parameter_name = 'max_latitude'
    field_name = 'parking_detail__latitude'


class MinLongitudeFilter(MinFilter):
    parameter_name = 'min_longitude'
    field_name = 'parking_detail__longitude'


class MaxLongitudeFilter(MaxFilter):
    parameter_name = 'max_longitude'
    field_name = 'parking_detail__longitude'


class MinTotalLotsFilter(MinFilter):
    parameter_name = 'min_total_lots'
    field_name = 'parking_detail__total_lots'


class MaxTotalLotsFilter(MaxFilter):
    parameter_name = 'max_total_lots'
    field_name = 'parking_detail__total_lots'


class MinAvailableLotsFilter(MinFilter):
    parameter_name = 'min_available_lots'
    field_name = 'parking_detail__available_lots'


class MaxAvailableLotsFilter(MaxFilter):
    parameter_name = 'max_available_lots'
    field_name = 'parking_detail__available_lots'


class MinPricePerHourFilter(MinFilter):
    parameter_name = 'min_price_per_hour'
    field_name = 'parking_detail__price_per_hour'


class MaxPricePerHourFilter(MaxFilter):
    parameter_name = 'max_price_per_hour'
    field_name = 'parking_detail__price_per_hour'


class FirstNameFilter(ContainFilter):
    parameter_name = 'first_name'
    field_name = 'user_detail__first_name'


class SecondNameFilter(ContainFilter):
    parameter_name = 'second_name'
    field_name = 'user_detail__second_name'


class ThirdNameFilter(ContainFilter):
    parameter_name = 'third_name'
    field_name = 'user_detail__third_name'


class EmailFilter(ContainFilter):
    parameter_name = 'email'
    field_name = 'user_detail__email'


class IsStaffFilter(BooleanExactFilter):
    parameter_name = 'is_staff'
    field_name = 'user_detail__is_staff'


class UserIdFilter(ExactFilter):
    parameter_name = 'user_id'
    field_name = 'user_id'


class ParkingIdFilter(ExactFilter):
    parameter_name = 'parking_id'
    field_name = 'parking_id'
