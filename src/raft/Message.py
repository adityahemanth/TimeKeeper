class Message(object):
    
    def __init__(self, type, payload):
        self.type = type
        self.payload = payload

    def getType(self):
        return self.type

    def getPayload(self):
        return self.payload