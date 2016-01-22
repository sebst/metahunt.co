from apis.angel import AngelList
from apis.crunch import CrunchBase
from apis.betalist import BetaList

from django.conf import settings


ANGEL = AngelList(settings.ANGEL_SECRET)
CRUNCH = CrunchBase(settings.CRUNCH_SECRET)
BETALIST = BetaList(settings.BETALIST_SECRET)
