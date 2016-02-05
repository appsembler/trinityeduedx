from django.forms import ModelForm, ChoiceField
from django.db.models.fields import BLANK_CHOICE_DASH

from .models import TrinityUserProfile
from .app_settings import DISTRICT_CHOICES


class TrinityUserProfileExtensionForm(ModelForm):

    # b/c of the way the registration extra fields code works,
    # must explicitly specify ChoiceField
    district = ChoiceField(label='School District', choices=BLANK_CHOICE_DASH + list(DISTRICT_CHOICES))

    def __init__(self, *args, **kwargs):
        super(TrinityUserProfileExtensionForm, self).__init__(*args, **kwargs)
        self.fields['district'].error_messages = {
            "required": u"Please indicate your school district.",
        }

    class Meta(object):
        model = TrinityUserProfile
        fields = ('district', )
