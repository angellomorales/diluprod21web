import os
from django.core.management.base import BaseCommand

from Basic.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:    
            username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
            print('Creating account for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')