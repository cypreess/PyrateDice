# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20141025_0017'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BoardStates',
            new_name='BoardState',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='url',
            field=models.URLField(help_text=b'Provide URL of your gamer service: http://...', null=True, blank=True),
            preserve_default=True,
        ),
    ]
