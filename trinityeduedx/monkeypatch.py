import logging
from django.conf import settings


log = logging.getLogger(__name__)


# set a HOMEPAGE_COURSE_MAX setting from ENV VARS
# avoid making this change in edx-platform and patch instead

log.info("""
	Monkey-patching settings.HOMEPAGE_COURSE_MAX.  Deprecate this when 
	edx-platform supports setting this from ENV tokens in lms/envs/aws.py
"""
)

env_setting = settings.ENV_TOKENS.get('HOMEPAGE_COURSE_MAX', None)
settings.HOMEPAGE_COURSE_MAX = env_setting
