class Pbbox(object):

    def __init__(self, x0, y0, x1, y1, text, typeb, signed_val=0):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.text = text
        self.typeb = typeb
        self.signed_val = signed_val
