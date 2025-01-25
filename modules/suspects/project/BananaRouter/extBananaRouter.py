'''Info Header Start
Name : extBananaRouter
Author : Wieland@AMB-ZEPH15
Saveorigin : DevUtils.toe
Saveversion : 2023.12000
Info Header End'''
from classRoute import Route
from Exceptions import *
from enum import Enum

class Init(Route):
	Name = "Init"
	Path = "/"

class Mode(Enum):
	Idle = "IDLE"
	CheckTransition = "PRETRANSITION"
	Transition = "TRANSITION"
	Abort = "ABORT"

class extBananaRouter:
	"""
	extBananaRouter description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.log = self.ownerComp.op("logger").Log
		self.ownerComp.op("Emitter").Attach_Emitter(self)
		
		self._ActiveRoute = tdu.Dependency(Init("", {}))
		self.TargetRoute = None # Make dependable. Someday...

		self._Mode = tdu.Dependency( Mode.Idle )
		self.Push( self.ownerComp.par.Initroute.eval() )

	@property
	def Mode(self):
		return self._Mode.val

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

	@property
	def asyncio(self):
		return self.ownerComp.op("asyncIODependency").GetGlobalComponent()

	def Push( self, uri , isAsync = True, meta = {}):
		if isAsync:
			return self.asyncio.RunAsync( self._Push( uri, meta ))
		return self.asyncio.RunSync( self._Push( uri, meta ))
	
	async def _Push(self, uri, meta):

		self._TargetRoute:Route = None
		self.log("Pushing", uri)
		for routeClass in self.routes:
			try:
				self._TargetRoute = routeClass( uri, meta )
			except Missmatch:
				continue
			break
		else:
			# This will be reached if we do not break the loop.
			self.log("No Matching Route found.")
			return False
			# raise Missmatch(f"No valid Routeobject defined for {uri}")
		self.log("Matching route found", self._TargetRoute.Name)
		self._Mode.val = Mode.CheckTransition
		self.log("Transition from", self.ActiveRoute)
		try:
			self.log("Checking valid values", self.ActiveRoute, self._TargetRoute)
			await self.ActiveRoute.preExit(self._TargetRoute, self.ownerComp)
			await self._TargetRoute.preEnter(self.ActiveRoute, self.ownerComp)
		except Abort as abortion:

			self._Mode.val = Mode.Abort

			self.log("Transition got aborted", abortion.with_traceback())
			self.Emit("TransitionAbort", self.ActiveRoute, self._TargetRoute, self.ownerComp)
			if abortion.redirect: 
				await self._Push( abortion.redirect )
			
			self._Mode.val = Mode.Idle

			return False
		except Exception as e:
			self._Mode.val = Mode.Idle
			raise e
		
		self._Mode.val = Mode.Transition
		self.log("Valid transition. Going in to transition mode and exeting current route.")
		await self.ActiveRoute.onExit(self._TargetRoute, self.ownerComp)
		self.Emit(f"RouteExit_{self.ActiveRoute.Name}", self.ActiveRoute, self._TargetRoute, self.ownerComp)

		self.log("Exited current state, en route!")

		self.Emit("RouteChange", self.ActiveRoute, self._TargetRoute, self.ownerComp)

		self.log("Entering Transition")
		await self._TargetRoute.onEnter(self.ActiveRoute, self.ownerComp)
		self.Emit(f"RouteEnter_{self._TargetRoute.Name}", self.ActiveRoute, self._TargetRoute, self.ownerComp)
		self.log("On new route")
		self.ownerComp.op("history").appendRow(self._TargetRoute._uri)
		
		self.log("DOne, cleaning up.")
		self._ActiveRoute.val = self._TargetRoute
		self._TargetRoute:Route = None

		self._Mode.val = Mode.Idle