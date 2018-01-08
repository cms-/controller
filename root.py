import db
import sys

class Root():

	def __init__(self, id, name, branch_table, table=None):
		self.id = id
		self.name = name
		self.table = table
		self.branch_table = branch_table
		self.branches = {}

	def getBranches(table, xref_id=1, xref_col='active'):
		sql = '''SELECT * FROM ''' + table + ''' WHERE ''' + xref_col + '''=:xref_id;'''
		args = {"xref_id": xref_id}
		#print (sql, args)
		resources = db.query(sql, args)
		return resources

	def addBranches(self, branches):
		for branch in branches:
			self.branches.update({branch[0]: getattr(sys.modules[__name__], self.branch_table.capitalize())(branch[0], branch[1])})

	def __str__(self):
		return "\t\t%s id: %i name: %s branch_table: %s " % (self.table, self.id, self.name, self.branch_table)

	def listBranches(self):
		print (self.name + " \\")
		for key, branch in self.branches.items():
			print (branch)

	def iterBranches(self, branch_id, branch_table):
		print("not yet")


class Trunk(Root):

	def __init__(self):
		Root.__init__(self, 0, 'Trunk', 'node')
		branches = Root.getBranches(self.branch_table)
		Root.addBranches(self, branches)


class Node(Root):

	def __init__(self, id, name):
		Root.__init__(self, id, name, 'service', 'node')
		branches = Root.getBranches(self.branch_table, self.id, self.table + "_id")
		Root.addBranches(self, branches)
		self.listBranches()


class Service(Root):

	def __init__(self, id, name):
		Root.__init__(self, id, name, 'resource', 'service')
		branches = Root.getBranches(self.branch_table, self.id, self.table + "_id")
		Root.addBranches(self, branches)
		self.listBranches()

class Resource(Root):

	def __init__(self, id, name):
		Root.__init__(self, id, name, None, 'resource')


trunk = Trunk()
trunk.listBranches()