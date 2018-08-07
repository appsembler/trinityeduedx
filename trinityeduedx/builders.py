from collections import OrderedDict

from appsembler_reporting.reportgen.builders import (
    DemographicReportRowBuilder,
)
from trinityeduedx.models import TrinityUserProfile
from trinityeduedx.serializers import TrinityUserProfileSerializer


def get_custom_serialized_data(user_id):
    """
    Gets the custom district data.
    """
    try:
        trinity_profile = TrinityUserProfile.objects.get(user_id=user_id)
        return TrinityUserProfileSerializer(trinity_profile).data
    except TrinityUserProfile.DoesNotExist:
        # Consider if we want to return an empty dict
        return None


class DemographicWithDistrictRowBuilder(DemographicReportRowBuilder):
    """
    This should be a final class (don't extend it)
    """

    fields = OrderedDict(DemographicReportRowBuilder.fields.items() + [
             ('district', 'custom_data.district'),
    ])

    def __init__(self, user_data):
        # Add trinity profile as a data source
        custom_data = get_custom_serialized_data(user_data['id'])
        sources = {
            'custom_data': custom_data,
        }

        super(DemographicWithDistrictRowBuilder, self).__init__(user_data, sources=sources)
