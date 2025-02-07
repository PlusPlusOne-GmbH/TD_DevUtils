
'''Info Header Start
Name : extConsitentReplicator
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : DevUtils.toe
Saveversion : 2023.12000
Info Header End'''

import tableUtils

class extConsitentReplicator:
	"""
	extConsitentReplicator description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.callback = self.ownerComp.op('callbackManager')
		if self.ownerComp.par.Active.eval(): 
			run( "me.Replicate()", fromOP=self.ownerComp, delayFrames = 1)


	@property
	def TemplateDAT(self):
		return self.ownerComp.par.Template.eval()
	
	def findReplicants(self):
		return tuple( self.ownerComp.par.Target.eval().findChildren( tags = [self.ownerComp.par.Replicatortag], maxDepth = 1 ) )
	
	def parseDatTemplate(self):
		templateList = tableUtils.tableToDict( self.TemplateDAT )
		namekey = self.ownerComp.par.Namekey.eval()
		return {
			tdu.legalName( item[ namekey ] ) : item for item in templateList
		}
	
	def Clear(self):
		for replicant in self.findReplicants():
			replicant.destroy()

	def prepareTemplate(self, template:dict):
		return { key : {
			**template[key], 
			**{"_index" : index} }
			 for index, key in enumerate( template ) }

	def Replicate(self, preClear:bool = False, template:dict = {}, iter = False):
		if preClear: self.Clear()
		template = template or self.parseDatTemplate()
		template = self.prepareTemplate( template )
		self.huntExistingReplicants(	template)
		if iter:
			for replicant in self.createMissingReplicants_Iter(	template ):
				yield replicant
		else:
			return self.createMissingReplicants( template )
		return
		
	def huntExistingReplicants(self, template):
		for hunted in self.findReplicants():
			if hunted.name in template: continue
			hunted.destroy()
	
	def createMissingReplicants(self, template):
		target = self.ownerComp.par.Target.eval()
		newReplicants = []
		for replicantName, replicantTemplate in template.items():
			if target.op(replicantName): continue
			newReplicants.append(
				self.createReplicant( replicantName, replicantTemplate, target )
			)
		return newReplicants

	def createMissingReplicants_Iter(self, template):
		target = self.ownerComp.par.Target.eval()
		for replicantName, replicantTemplate in template.items():
			if target.op(replicantName): continue
			yield self.createReplicant( replicantName, replicantTemplate, target )
			
	def createReplicant(self, name:str, template:dict, target):
		self.callback.Do_Callback( "onPreCreate", template, self.ownerComp )
		newReplicant = target.copy( self.ownerComp.par.Blueprint.eval(), name = name)
		newReplicant.tags.add( self.ownerComp.par.Replicatortag.eval() )
		self.callback.Do_Callback( "onNewReplicant", newReplicant, template, self.ownerComp )
		return newReplicant, template
			
			
			
			
			
			
			
			
			
			
			
			
			
			