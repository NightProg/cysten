import enum

class License(enum.Enum):
    GNU_AGPLv3 = 1
    GNU_GPLv3 = 2
    GNU_LGPLv3 = 3
    Mozilla_Public_License_2_0 = 4
    Apache_License_2_0 = 5
    MIT_License = 6
    Boost_Software_License_1_0 = 7
    The_Unlicense = 8
    No_License = 9
    Other = 10

    def from_string(license):
        license = license.replace(" ", "_")
        if license not in License.__members__:
            return License.Other
        return License[license]

    def __str__(self):
        return self.name.replace("_", " ")