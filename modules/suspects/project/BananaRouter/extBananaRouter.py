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

		if not matchedRoute:
			self.log("No Matching Route found.")
			return False
			# raise Missmatch(f"No valid Routeobject defined for {uri}")
		
		if self.ActiveRoute:
			try:
				self.ActiveRoute.preExit(matchedRoute, self.ownerComp)
			except (Abort, Suspend) as e:
				self.log("PreExit guard failed.", e)
				return False

		try:
			matchedRoute.preEnter(self.ActiveRoute, self.ownerComp)
		except (Abort, Suspend) as e:
			self.log("PreEnter guard failed.", e)
			return False
		
		self.ownerComp.op("history").appendRow(matchedRoute._uri)
		self.Emit("RouteChange", self.ActiveRoute, matchedRoute, self.ownerComp)
		self._ActiveRoute.val = matchedRoute