"""
Reusable mixins for XBlocks and/or XModules
"""

from django.conf import settings
from xblock.fields import Scope, String, Float, XBlockMixin

# Make '_' a no-op so we can scrape strings
_ = lambda text: text


CREDITS_VIEW = 'credits_view'

# this is included as a mixin in xmodule.course_module.CourseDescriptor

class CreditsMixin(XBlockMixin):
    """
    Mixin that allows an author to specify a credit provider and a number of credit
    units.
    """
    credit_provider = String(
        display_name=_("Credit Provider"),
        help=_("Name of the entity providing the credit units"),
        default="",
        scope=Scope.settings,
    )

    credits = Float(
        display_name=_("Credits"),
        help=_("Hours or other unit of credits"),
        default=None,
        scope=Scope.settings,
    )
