'''Info Header Start
Name : classRoute
Author : Wieland@AMB-ZEPH15
Saveorigin : DevUtils.toe
Saveversion : 2023.12000
Info Header End'''

from Exceptions import Suspend, Abort, Missmatch
from typing import final
from argparse import Namespace

# from extBananaRouter import extBananaRouter

class Route():

    def __init__(self, uri, meta):
        if not self.Name: raise ("Name Attribute needs to be defined.")
        if not self.Path: raise ("Path Attribute needs to be defined.")
        self._uri = uri
        self._parseUri()
        self.Meta = meta

    def _parseUri(self):
        params = {}
        for pathElement, uriElement in zip(
            self.Path.strip("/").split("/"),
            self._uri.strip("/").split("/"),
            strict = True
        ):
            if pathElement.startswith(":"):
                params[pathElement.strip(":")] = uriElement
                continue
            if pathElement.lower() == uriElement.lower():
                continue
            raise Missmatch
        self.Params = Namespace(**params)
            
    Meta : dict
    Name : str
    Path : str    

    
    AllowedTransition : list[str] = ["*"] 

    @property
    def Uri(self):
        return self._uri

    @staticmethod
    @final
    def Abort( reason = "" ):
        raise Abort(reason)


    async def preEnter(self, source:"Route", router:"extBananaRouter" ) -> bool:
        """
            Gets run after preExit of sourceroute is run.
            call self.Suspend() or self.Abort() to halt transition.
        """
        pass
    
    async def onEnter(self, source:"Route", router:"extBananaRouter" ) -> bool:
        """
            Gets executed if all prechecks pass.
        """
        pass  

    async def preExit(self, target:"Route", router:"extBananaRouter") -> bool:
        """ 
            Gets run before preEnter of target route is run.
            call self.Suspend() or self.Abort() to halt transition.
        """
        pass

    async def onExit(self, target:"Route", router:"extBananaRouter") -> bool:
        """ 
            Gets executed if all prechecks pass.
        """
        pass

    