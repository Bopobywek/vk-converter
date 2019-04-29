class RequestHandler(object):

    def __init__(self, data):
        self.data = data
        self.object = self.get_object()

    def get_object(self):
        if isinstance(self.data, dict):
            return self.data.get('object')

    def get_user_id(self):
        if isinstance(self.data, dict):
            return self.object
