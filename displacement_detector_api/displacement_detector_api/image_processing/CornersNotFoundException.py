class CornersNotFoundException(Exception):

    def __init__(self, msg):
        super(CornersNotFoundException, self).__init__(msg)