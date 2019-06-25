from math import isnan

def iterable(it, exception=None):
	"""Returns 'True' if 'it' is iterable, 'False' otherwise"""
	
	try:
		iter(it)
		return True

	except TypeError:
		if exception is None:
			return False
		else:
			raise exception

def between(lower, var, upper):
	"""Returns 'True' if 'var' is between 'lower' and 'upper', 'False' 
	otherwise"""
	return lower < var and var < upper

def always_true(var):
	"""Returns 'True'"""
	return True