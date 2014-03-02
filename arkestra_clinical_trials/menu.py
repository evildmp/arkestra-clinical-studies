from models import TrialEntity
from lister import TrialsMenuLister


class TrialMenu(object):
    url = "clinical-trials"

    always_publish = True
    sub_menus = None
    lister = TrialsMenuLister
    model = TrialEntity

    menu_title = "Clinical trials"
