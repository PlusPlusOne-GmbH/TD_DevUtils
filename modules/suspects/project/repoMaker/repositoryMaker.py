'''Info Header Start
Name : repositoryMaker
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

class repositoryMaker:
	"""
	repositoryMaker description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def Reset(self):
		self.repoParameter.val = self.prefabOperator

	def InitOwner(self):
		page = self.find_repo_page()
		opParaeter = page.appendOP( 		
			self.OperatorParName,
			label = self.ownerName, 
			replace=True)
		opParaeter.val = self.prefabOperator
		opParaeter[0].startSection  = True
		page.appendPulse( 	
			self.CreateParName,
			label = "Create", 
			replace=True)
		return
	
	@property
	def OperatorParName(self):
		return f"{self.ownerName.capitalize()}repositorie"

	@property
	def CreateParName(self):
		return f"{self.ownerName.capitalize()}create"

	@property
	def Owner(self):
		return self.ownerComp.par.Owner.eval()

	@property
	def ownerName(self):
		return self.ownerComp.par.Name.eval()

	@property 
	def repoParameterVal(self):
		return self.repoParameter.eval()
	
	@property
	def repoParameter(self):
		return self.Owner.par[self.OperatorParName]
	
	@property
	def Repo(self):
		if self.Initialized:
			if self.Owner.par.Autocreate.eval() and self.repoParameterVal == self.prefabOperator: self.Create_Repo()
			return self.repoParameterVal
		return None

	@property
	def prefabOperator(self):
		return self.Owner.par.Prefab.eval()

	@property
	def Initialized(self):
		return hasattr( self.Owner.par, self.OperatorParName )

	def Reevaluate(self):
		if self.Owner.par[ self.OperatorParName ].eval(): return
		self.Owner.par[ self.OperatorParName ].val = self.prefabOperator
		return

	def Create_Repo(self):
		x_offset 	= 0
		for docked_op in self.Owner.docked:
			x_offset += docked_op.nodeWidth + 20
		repo 		= self.Owner.parent().copy( self.prefabOperator, name = f"{self.Owner.name}_{self.ownerName}")
		repo.nodeX 	= self.Owner.nodeX + x_offset
		repo.nodeY 	= self.Owner.nodeY - ( repo.nodeHeight + 20 )
		repo.dock 	= self.Owner
		self.Owner.par[self.OperatorParName].val = repo
		return

	def find_repo_page(self):
		pagename = self.Owner.par.Pagename.eval() or "Repositorie"
		for page in self.Owner.customPages:
			if page.name == pagename:
				return page
		return self.Owner.appendCustomPage( pagename )
	