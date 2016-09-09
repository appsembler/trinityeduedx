"""
Pass a cert_data.yml file and parse the values of 
CREDITS_NUM and CREDITS_PROVIDER into the Course's
credits and credit_provider fields.  
"""

import os
import optparse
import traceback

import yaml

from django.core.management.base import BaseCommand, CommandError
from django.http import Http404

from xmodule.modulestore.exceptions import ItemNotFoundError
from xmodule.modulestore.django import modulestore

from opaque_keys.edx.keys import CourseKey
from opaque_keys import InvalidKeyError
from courseware.courses import get_course_by_id


class Command(BaseCommand):
    help = """Reads course certificate data from a cert_data.yml file and loads
credits and credit_provider values to course fields.  Run it this way:
./manage.py cms --settings aws migrate_cert_data_to_course_fields --data /edx/app/certs/openedx-custom-certs/cert_data.yml.
The data file must be readable by the edxapp user.
You can optionally pass the --dry-run option to see what changes would be made without affecting the database.
    """

    data_option = optparse.make_option('--data',
                                action='store',
                                dest='data',
                                default=False,
                                help='valid --data <file path> required, e.g. --data /edx/app/certs/edx-custom-certs/cert-data.yml')
    dryrun_option = optparse.make_option('--dry-run',
                                action='store_true',
                                dest='dry-run',
                                default=False,
                                help='--dry-run (optional)')

    option_list = BaseCommand.option_list + (data_option, dryrun_option)    


    def handle(self, *args, **options):
        if not options['data'] or not os.path.isfile(options['data']):
            raise CommandError(Command.data_option.help)


        def stdout(msg, style=self.style.NOTICE):
            self.stdout.write(style(msg))
        
        print 'Trying to migrate credits data from YAML file at {0} to course module fields.'.format(options['data'])

        try:
            output = ""
            commit = options.has_key('dry-run')

            # read the cert data
            f = file(options['data'], 'r')
            data = yaml.load(f)
            store = modulestore()

            # loop through course ids and populate fields in corresponding course modules
            for k,v in data.items():
                try:
                    coursekey = CourseKey.from_string(k)
                    course = get_course_by_id(coursekey)
                except (Http404, InvalidKeyError):
                    stdout('No course matched key {0}.  Continuing...'.format(k))
                    continue

                credits = v.has_key('CREDITS_NUMBER') and v['CREDITS_NUMBER'] or course.credits
                provider = v.has_key('CREDITS_PROVIDER') and v['CREDITS_PROVIDER'] or course.credit_provider

                if commit:
                    course.credits = credits
                    course.credit_provider = provider
                    course.save()
                    store.update_item(course, course._edited_by)
                    
                output += "\tMigrated to {course} w/ data: credits:{credits}, provider:{provider}\n".format(course=k,credits=credits,provider=provider)

            if not commit:
                stdout(self.style.NOTICE('Completed dry-run migration of cert data to course fields. Would have migrated the following:\n{0}\n\n'.format(output)))
            else:
                stdout(self.style.NOTICE('Successfully ran migration of cert data to course fields.\n{0}\n\n'.format(output)))
        except:  # pylint: disable=broad-except
            trace = traceback.format_exc()
            stdout("Couldn't migrate: error occurred at key: '{}'. error was {}".format(k, trace))
            raise CommandError('Could not complete migration of cert data to course fields.')
