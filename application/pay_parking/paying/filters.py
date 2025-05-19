from pay_parking.filters import (
    ContainFilter, ExactFilter, MinFilter, MaxFilter,
    MaxHourDurationFilter, MinHourDurationFilter, BooleanExactFilter,
    IntergerExactFilter
)


class MinCreatedAtFiler(MinFilter):
    parameter_name = 'min_created_at'
    field_name = 'created_at'


class MaxCreatedAtFiler(MaxFilter):
    parameter_name = 'max_created_at'
    field_name = 'created_at'


class MinStartFiler(MinFilter):
    parameter_name = 'min_start'
    field_name = 'start'


class MaxStartFiler(MaxFilter):
    parameter_name = 'max_start'
    field_name = 'end'


class MinEndFiler(MinFilter):
    parameter_name = 'min_end'
    field_name = 'end'


class MaxEndFiler(MaxFilter):
    parameter_name = 'max_end'
    field_name = 'end'


class MinPriceFiler(MinFilter):
    parameter_name = 'min_price'
    field_name = 'price'


class MaxPriceFiler(MaxFilter):
    parameter_name = 'max_price'
    field_name = 'price'


class MinDurationFiler(MinHourDurationFilter):
    parameter_name = 'min_duration'
    field_name = 'duration'


class MaxDurationFiler(MaxHourDurationFilter):
    parameter_name = 'max_duration'
    field_name = 'duration'


class AddressFiler(ContainFilter):
    parameter_name = 'address'
    field_name = 'parking_detail__address'


class ParkingZoneFiler(IntergerExactFilter):
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


class MinPricePerHourFilter(MinFilter):
    parameter_name = 'min_price_per_hour'
    field_name = 'parking_detail__price_per_hour'


class MaxPricePerHourFilter(MaxFilter):
    parameter_name = 'max_price_per_hour'
    field_name = 'parking_detail__price_per_hour'


class FirstNameFiler(ContainFilter):
    parameter_name = 'first_name'
    field_name = 'user_detail__first_name'


class SecondNameFiler(ContainFilter):
    parameter_name = 'second_name'
    field_name = 'user_detail__second_name'


class ThirdNameFiler(ContainFilter):
    parameter_name = 'third_name'
    field_name = 'user_detail__third_name'


class EmailFiler(ContainFilter):
    parameter_name = 'email'
    field_name = 'user_detail__email'


class IsStaffFiler(BooleanExactFilter):
    parameter_name = 'is_staff'
    field_name = 'user_detail__is_staff'


class UserIdFiler(ExactFilter):
    parameter_name = 'user_id'
    field_name = 'user_id'


class ParkingIdFiler(ExactFilter):
    parameter_name = 'user_id'
    field_name = 'user_id'
