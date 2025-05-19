from pay_parking.filters import ContainFilter, ExactFilter, MinFilter, MaxFilter

class AddressFilter(ContainFilter):
    parameter_name = 'address'
    field_name = 'address'


class ParkingZoneFilter(ExactFilter):
    parameter_name = 'parking_zone'
    field_name = 'parking_zone'


class MinLatitudeFilter(MinFilter):
    parameter_name = 'min_latitude'
    field_name = 'latitude'


class MaxLatitudeFilter(MaxFilter):
    parameter_name = 'max_latitude'
    field_name = 'latitude'


class MinLongitudeFilter(MinFilter):
    parameter_name = 'min_longitude'
    field_name = 'longitude'


class MaxLongitudeFilter(MaxFilter):
    parameter_name = 'max_longitude'
    field_name = 'longitude'


class MinTotalLotsFilter(MinFilter):
    parameter_name = 'min_total_lots'
    field_name = 'total_lots'


class MaxTotalLotsFilter(MaxFilter):
    parameter_name = 'max_total_lots'
    field_name = 'total_lots'


class MinAvailableLotsFilter(MinFilter):
    parameter_name = 'min_available_lots'
    field_name = 'available_lots'


class MaxAvailableLotsFilter(MaxFilter):
    parameter_name = 'max_available_lots'
    field_name = 'available_lots'


class MinPricePerHourFilter(MinFilter):
    parameter_name = 'min_price_per_hour'
    field_name = 'price_per_hour'


class MaxPricePerHourFilter(MaxFilter):
    parameter_name = 'max_price_per_hour'
    field_name = 'price_per_hour'
