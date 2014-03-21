from models import StudyEntity
from lister import StudiesMenuLister


class StudyMenu(object):
    # this must match the url for an entity's view of its clinical trials in
    # urls.py
    url = "clinical-studies"

    # We have to make two important decisions here. Should we check:
    # 1. for each Entity, whether this item will appear in its menu?
    #    entity_model:
    #    if entity_model is not specified, we can create the menu item;
    #    otherwise, consult the entity_model instance for this entity
    # 2. if there's anything to display before creating the menu item?
    #    lister:
    #    if lister is not specified, we can create the menu item; otherwise we
    #    have to invoke the lister that checks if there's anything to display

    entity_model = StudyEntity
    lister = StudiesMenuLister

    # Other attributes:
    #
    # If we're not using an entity_model with a menu_title attribute, we must
    # provide that here, for example:
    #
    # menu_title = "Clinical trials"
    #
    # Optionally, if using a lister, we can make a menu node for each of the
    # lister's lists' other_items() (if they exist)
    #
    # sub_menus = True
