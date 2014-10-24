# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20141024_2123'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardStates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iteration', models.IntegerField(db_index=True)),
                ('data', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='url',
            field=models.URLField(help_text=b'Provide http url of your machine', null=True, blank=True),
            preserve_default=True,
        ),
    ]
