'''Info Header Start
Name : Exceptions
Author : Wieland@AMB-ZEPH15
Saveorigin : DevUtils.toe
Saveversion : 2023.12000
Info Header End'''
class Suspend(Exception):
    pass

class Abort(Exception):
    def __init__(self, *args, redirect = ""):
        super().__init__(*args)
        self.redirect = redirect
    pass

class Missmatch(Exception):
    pass