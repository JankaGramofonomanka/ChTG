from math import isnan

def iterable(it, exception=None):
	
	try:
		iter(it)
		return True

	except TypeError:
		if exception is None:
			return False
		else:
			raise exception

def between(lower, var, upper):
	return lower < var and var < upper

def always_true(var):
	return True