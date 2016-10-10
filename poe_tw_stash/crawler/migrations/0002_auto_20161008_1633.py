# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicItem',
            fields=[
                ('socketedItems', models.TextField(default=b'')),
                ('corrupted', models.BooleanField(default=False)),
                ('typeLine', models.TextField(default=b'')),
                ('talismanTier', models.IntegerField(default=-1)),
                ('flavourText', models.TextField(default=b'')),
                ('id', models.CharField(default=b'', max_length=128, serialize=False, primary_key=True)),
                ('lockedToCharacter', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('support', models.BooleanField(default=False)),
                ('secDescrText', models.TextField(default=b'')),
                ('sockets', models.TextField(default=b'')),
                ('duplicated', models.TextField(default=True)),
                ('frameType', models.TextField(default=-1)),
                ('nextLevelRequirements', models.TextField(default=b'')),
                ('descrText', models.TextField(default=b'')),
                ('inventoryId', models.CharField(default=b'', max_length=64)),
                ('icon', models.TextField(default=b'')),
                ('league', models.IntegerField(default=0, choices=[(0, '\u6a19\u6e96\u6a21\u5f0f'), (1, '\u5c08\u5bb6\u6a21\u5f0f'), (2, '\u7cbe\u9ad3\u806f\u76df'), (3, '\u7cbe\u9ad3\u806f\u76df\uff08\u5c08\u5bb6\uff09')])),
                ('artFilename', models.TextField(default=b'')),
                ('name', models.CharField(default=b'', max_length=64)),
                ('identified', models.BooleanField(default=False)),
                ('h', models.IntegerField(default=-1)),
                ('w', models.IntegerField(default=-1)),
                ('x', models.IntegerField(default=-1)),
                ('y', models.IntegerField(default=-1)),
                ('z', models.IntegerField(default=-1)),
                ('requirements', models.TextField(default=b'')),
                ('ilvl', models.IntegerField(default=-1)),
                ('properties', models.TextField(default=b'')),
                ('additionalProperties', models.TextField(default=b'')),
                ('craftedMods', models.TextField(default=b'')),
                ('implicitMods', models.TextField(default=b'')),
                ('explicitMods', models.TextField(default=b'')),
                ('cosmeticMods', models.TextField(default=b'')),
                ('enchantMods', models.TextField(default=b'')),
                ('note', models.TextField(default=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Stash',
            fields=[
                ('stashType', models.CharField(default=b'', max_length=128)),
                ('stash', models.CharField(default=b'', max_length=128)),
                ('accountName', models.CharField(default=b'', max_length=128)),
                ('public', models.BooleanField(default=True)),
                ('lastCharacterName', models.CharField(default=b'', max_length=128)),
                ('id', models.CharField(default=b'', max_length=128, serialize=False, primary_key=True)),
                ('items', models.ManyToManyField(related_name='item_stash', to='crawler.BasicItem')),
            ],
        ),
        migrations.DeleteModel(
            name='EssenceHardcoreItem',
        ),
        migrations.DeleteModel(
            name='EssenceItem',
        ),
        migrations.DeleteModel(
            name='StandardHardcoreItem',
        ),
        migrations.DeleteModel(
            name='StandardItem',
        ),
    ]
