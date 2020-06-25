
class Element(object):
    #lister = []
    def __init__(self, elementId, playerEmail, actionType, creationTimestamp, moreAttributes):
        self.elementId = elementId
        self.playerEmail = playerEmail
        self.actionType = actionType
        self.creationTimestamp = creationTimestamp
        self.moreAttributes = moreAttributes

