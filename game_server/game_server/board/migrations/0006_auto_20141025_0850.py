# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_auto_20141025_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='url',
            field=models.URLField(help_text=b'Provide URL of your gamer service: http://...', max_length=150, null=True, blank=True),
            preserve_default=True,
        ),
    ]
