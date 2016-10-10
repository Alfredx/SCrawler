# -*- coding: utf-8 -*-
# author: ShenChao

from django.db import models


class AbstractTable(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Stash(AbstractTable):
    stashType = models.CharField(max_length=128, default='', null=True)
    stash = models.CharField(max_length=128, default='', null=True)
    accountName = models.CharField(max_length=128, default='', null=True)
    public = models.BooleanField(default=True)
    lastCharacterName = models.CharField(max_length=128, default='')
    id = models.CharField(max_length=128, default='', primary_key=True)
    items = models.ManyToManyField('BasicItem', related_name='item_stash')


class BasicItem(AbstractTable):
    league_choice = ((0, u'標準模式'),
                     (1, u'專家模式'),
                     (2, u'精髓聯盟'),
                     (3, u'精髓聯盟（專家）'),)

    socketedItems = models.TextField(default='')
    corrupted = models.BooleanField(default=False)
    typeLine = models.TextField(default='')
    talismanTier = models.IntegerField(default=-1)
    flavourText = models.TextField(default='')
    id = models.CharField(max_length=128, default='', primary_key=True)
    lockedToCharacter = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    support = models.BooleanField(default=False)
    secDescrText = models.TextField(default='')
    sockets = models.TextField(default='')
    duplicated = models.TextField(default=True)
    frameType = models.TextField(default=-1)
    nextLevelRequirements = models.TextField(default='')
    descrText = models.TextField(default='')
    inventoryId = models.CharField(default='', max_length=64)
    icon = models.TextField(default='')
    league = models.IntegerField(choices=league_choice, default=0)
    artFilename = models.TextField(default='')
    name = models.CharField(default='', max_length=64)
    identified = models.BooleanField(default=False)
    h = models.IntegerField(default=-1)
    w = models.IntegerField(default=-1)
    x = models.IntegerField(default=-1)
    y = models.IntegerField(default=-1)
    z = models.IntegerField(default=-1)

    requirements = models.TextField(default='')
    ilvl = models.IntegerField(default=-1)
    properties = models.TextField(default='')
    additionalProperties = models.TextField(default='')
    craftedMods = models.TextField(default='')
    implicitMods = models.TextField(default='')
    explicitMods = models.TextField(default='')
    cosmeticMods = models.TextField(default='')
    enchantMods = models.TextField(default='')

    note = models.TextField(default='')

    @classmethod
    def toleague(self, s):
        l = [u'標準模式', u'專家模式', u'精髓聯盟', u'精髓聯盟（專家）']
        try:
            return l.index(s)
        except Exception, e:
            return 0
