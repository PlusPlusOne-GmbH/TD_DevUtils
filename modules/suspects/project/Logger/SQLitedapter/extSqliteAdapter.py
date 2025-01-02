'''Info Header Start
Name : extSqliteAdapter
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.12000
Info Header End'''

import sqlite3
from functools import cache
from pathlib import Path
from typing import Set
from threading import Thread


class extSqliteAdapter:
	"""
	extSqliteAdapter description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.checkDelay = None
		self.committedConnections:Set[sqlite3.Connection] = set()
		self.log = self.ownerComp.op("oldLogger").Log
	
	def __delTD__(self):
		self.GetCursor.cache_clear()
			# cachedResult.close()

	@cache
	def GetCursor(self, databasePath, **requiredTables):
		self.log("Creating database", databasePath)
		databasePathObject = Path(
			databasePath
		)
		databasePathObject.parent.mkdir( exist_ok=True, parents=True)

		connector = sqlite3.connect(
			databasePathObject, 
			check_same_thread = False #YOLO!!
			)

		cursor = connector.cursor()
		for key, value in requiredTables.items():
			cursor.execute(f"""
				 CREATE TABLE 
				 IF NOT EXISTS 
				 {key}({','.join(value)})
				 """)
		self.log("Returning Cursor")
		return cursor
	
	def Commit(self, cursor:sqlite3.Cursor):
		self.log("Comitting Cursor")
		self.committedConnections.add( cursor.connection )
		if not self.checkDelay:
			self.checkDelay = run(
				"args[0]()", self._check, delayFrames = 1
			)
	
	def _check(self):
		self.log("Running commitmentthread")
		Thread(target=self._threadCommit, args = (self.committedConnections.copy(),) ).start()
		
		# for connection in self.committedConnections:
		#	connection.commit()
		
		self.committedConnections.clear()
		self.checkDelay = None
		self.log("Cleared and thread running.")

	def _threadCommit(self, connections):
		for connection in connections:
			connection.commit()
		return