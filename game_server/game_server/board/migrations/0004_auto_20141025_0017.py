# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_auto_20141024_2333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boardstates',
            old_name='data',
            new_name='board_data',
        ),
        migrations.AddField(
            model_name='boardstates',
            name='state_data',
            field=jsonfield.fields.JSONField(default=dict),
            preserve_default=True,
        ),
    ]
