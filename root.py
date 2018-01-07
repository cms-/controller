import db
import sys

class Root():

	def __init__(self, id, name, branch_table, table=None):
		self.id = id
		self.name = name
		self.table = table
		self.branch_table = branch_table
		self.branches = list()

	def getBranches(table, xref_id=1, xref_table='active'):
		sql = '''SELECT * FROM ''' + table + ''' WHERE ''' + xref_table + '''=:xref_id;'''
		args = {"xref_id": xref_id}
		print (sql, args)
		resources = db.query(sql, args)
		return resources

	def __str__(self):
		return "%s id: %i name: %s branch_table: %s " % (self.table, self.id, self.name, self.branch_table)

	def listBranches(self):
		for branch in self.branches:
			print (branch)


class Viewer(Root):

	def __init__(self):
		Root.__init__(self, 0, 'Viewer', 'node')
		branches = Root.getBranches(self.branch_table)
		for branch in branches:
			self.branches.append(getattr(sys.modules[__name__], self.branch_table.capitalize())(branch[0], branch[1]))


class Node(Root):

	def __init__(self, id, name):
		Root.__init__(self, id, name, 'service', 'node')
		branches = Root.getBranches(self.branch_table, self.id, self.table + "_id")
		for branch in branches:
			self.branches.append(getattr(sys.modules[__name__], self.branch_table.capitalize())(branch[0], branch[1]))


class Service(Root):

	def __init__(self, id, name):
		Root.__init__(self, id, name, 'resource', 'service')


class Resource(Root):

	def nothing(self):
		print("nothing")


view = Viewer()
view.listBranches()