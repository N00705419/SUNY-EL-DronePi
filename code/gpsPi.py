class GpsPi(object):
	"""docstring for Gps"""
	def read(self):
		# temporary mock
		gpsData = {}
		gpsData['latitude'] = '41.7365927'
		gpsData['longitude'] = '-74.0874642'
		gpsData['altitude'] = '71'
		return gpsData