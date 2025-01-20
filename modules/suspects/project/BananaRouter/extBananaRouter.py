'''Info Header Start
Name : extBananaRouter
Author : Wieland@AMB-ZEPH15
Saveorigin : DevUtils.toe
Saveversion : 2023.12000
Info Header End'''
from classRoute import Route
from Exceptions import *

class Init(Route):
	Name = "Init"
	Path = "/"

class extBananaRouter:
	"""
	extBananaRouter description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.log = self.ownerComp.op("logger").Log
		self.ownerComp.op("Emitter").Attach_Emitter(self)
		self._ActiveRoute = tdu.Dependency(Init(""))

	@property
	def ActiveRoute(self):
		return self._ActiveRoute.val

	@property
	def routes(self) -> list[Route]:
		return self.ownerComp.op("callbackManager").Do_Callback(
			"defineRoutes", 
			self.ownerComp, 
			Route
		)

	def Push(self, uri):
		matchedRoute:Route = None
		self.log("Pushing", uri)
		for routeClass in self.routes:
			try:
				matchedRoute = routeClass( uri )
			except Missmatch:
				continue
			break
		else:
			# This will be reached if we do not break the loop.
			self.log("No Matching Route found.")
			return False
			# raise Missmatch(f"No valid Routeobject defined for {uri}")
		
		try:
			self.ActiveRoute.preExit(matchedRoute, self.ownerComp)
			matchedRoute.preEnter(self.ActiveRoute, self.ownerComp)
		except Abort as abortion:
			self.log("Transition got aborted", abortion.with_traceback())
			if abortion.redirect: self.Push( abortion.redirect )
			return False
		except Suspend as suspension:
			self.log("Got suspended", suspension.with_traceback())
			return False
		except Exception as e:
			raise e
		
		self.ActiveRoute.onExit(matchedRoute, self.ownerComp)
		self.Emit(f"RouteExit_{self.ActiveRoute.Name}", self.ActiveRoute, matchedRoute, self.ownerComp)

		self.Emit("RouteChange", self.ActiveRoute, matchedRoute, self.ownerComp)

		matchedRoute.onEnter(self.ActiveRoute, self.ownerComp)
		self.Emit(f"RouteEnter_{matchedRoute.Name}", self.ActiveRoute, matchedRoute, self.ownerComp)

		self.ownerComp.op("history").appendRow(matchedRoute._uri)
		self._ActiveRoute.val = matchedRoute