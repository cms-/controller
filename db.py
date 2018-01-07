from db_connection import the_sqlite_connection

def query(sql, args):
	# Can a query function handle both inserts and selects?
	# This one seems to be capable of such.
	# Suited to read-only access.
	with the_sqlite_connection as conn:
		try:
			curs = conn.cursor()
			curs.execute(sql,args)
			result = curs.fetchall()
			try:
				conn.commit()
			except:
				pass

			return result
		except Exception as error:
			print('caught this error: ' + repr(error))