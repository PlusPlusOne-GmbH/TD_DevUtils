


'''Info Header Start
Name : extCallbackManager
Author : Wieland@AMB-ZEPH15
Saveorigin : DevUtils.toe
Saveversion : 2023.12000
Info Header End'''

from functools import lru_cache
TDF = op.TDModules.mod.TDFunctions
import TDJSON

class extCallbackManager:
	"""
	extCallbackManager description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp : baseCOMP 	= ownerComp
		self.pageName : str 		= 'Callbacks'
		self.callbackTemplate : DAT = self.ownerComp.op('default_callbacks')
		self.Execute 				= self.GetMethod
		self.Do_Callback 			= self.DoCallback
	@property
	def owner(self) -> OP:
		return self.ownerComp.par.Owner.eval()
	
	@property
	def moduleOperator(self) -> DAT:
		return self.owner.par.Callbacks.eval()
	
	@property
	def callbackModule(self):
		return self.moduleOperator.module
	  
	def Reset(self):
		self.owner.par.Callbacks = self.callbackTemplate

	def InitOwner(self):
		prefab = { parameter.name : TDJSON.parameterToJSONPar( parameter ) for parameter  in self.ownerComp.op("parameter_prefab").customPars }
		try:
			callbacks_par = TDJSON.addParameterFromJSONDict( self.owner, prefab["Callbacks"], replace = False )
			callbacks_par.val = self.owner.relativePath(self.callbackTemplate)
		except tdError:
			pass

		try:
			create_par = TDJSON.addParameterFromJSONDict( self.owner, prefab["Createcallbacks"], replace = False )
		except tdError:
			pass

	def empty_callback(self, *args, **kwargs):
		return
	
	

	@lru_cache(maxsize=64)
	def getMethodCached(self, name, key):
		return self.getMethod( name )

	def getMethod(self, name):
		return getattr( self.callbackModule, name, self.empty_callback)

	def GetMethod(self, name, cached = True):
		if cached:
			return self.getMethodCached(
				name, self.moduleOperator.text
			)
		return self.getMethod( name )

	def DoCallback(self, name, *arguments, **keywordarguments):
		if self.ownerComp.par.Cache.eval():
			return self._CachedDoCallback(
				name, self.moduleOperator.text,
				*arguments,
				**keywordarguments
			)
		else:
			return self._DoCallback( 
				name, 
				*arguments, 
				**keywordarguments
			)
		
	@lru_cache(maxsize=64)
	def _CachedDoCallback(self, name, datText, *arguments, **keywordarguments):
		return self._DoCallback( name, *arguments, **keywordarguments)
	
	def _DoCallback(self, name, *arguments, **keywordarguments):
		try:
			return self.GetMethod(name)(*arguments, **keywordarguments)
		except Exception as e:
			if self.ownerComp.par.Gracefulerror.eval(): 
				self.ownerComp.op("logger").Log( "Error during callback execution", e)
				return None
			raise e

	def CreateCallbacks(self, owner):
		new_callback_dat = owner.parent().copy(self.ownerComp.op("emptyCallbacks"), name = f"{owner.name}_callbacks")
		new_callback_dat.text = self.callbackTemplate.text
		new_callback_dat.nodeX = owner.nodeX
		new_callback_dat.nodeY = owner.nodeY - 150
		new_callback_dat.dock = owner
		owner.par.Callbacks = new_callback_dat
		