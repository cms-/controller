import db
import sys

class Root():

	def __init__(self, id, name, branch_table, table=None):
		self.id = id
		self.name = name
		self.table = table
		self.branch_table = branch_table
		self.branches = {}

	def fetchBranches(table, xref_id=1, xref_col='active'):
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
		for value in Root.iterBranches(self):
			print(value)

	def getBranches(self):
		return self.branches

	def iterBranches(self):
		for value in self.branches.values():
			yield value


class Trunk(Root):

	def __init__(self):
		Root.__init__(self, 0, 'Trunk', 'node')
		branches = Root.fetchBranches(self.branch_table)
		Root.addBranches(self, branches)


class Node(Root):

	def __init__(self, id, name):
		Root.__init__(self, id, name, 'service', 'node')
		branches = Root.fetchBranches(self.branch_table, self.id, self.table + "_id")
		Root.addBranches(self, branches)


class Service(Root):

	def __init__(self, id, name):
		Root.__init__(self, id, name, 'resource', 'service')
		branches = Root.fetchBranches(self.branch_table, self.id, self.table + "_id")
		Root.addBranches(self, branches)

class Resource(Root):

	def __init__(self, id, name):
		Root.__init__(self, id, name, None, 'resource')


trunk = Trunk()
obj = trunk.getBranches()
trunk.listBranches()
for value in trunk.iterBranches():
	print(value)