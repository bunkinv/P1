import time
import functools


# tomorrow for threading & deco, showme for timing/usage stat


def timeit(method):
	def timed(*args, **kw):
		ts = time.time()
		result = method(*args, **kw)
		te = time.time()
		if 'log_time' in kw:
			name = kw.get('log_name', method.__name__.upper())
			kw['log_time'][name] = int((te - ts) * 1000)
		else:
			print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
		return result

	return timed


# use: import threading
# lock = threading.Lock()
def synchronized(lock):
	""" Synchronization decorator """

	def wrap(f):
		@functools.wraps(f)
		def newFunction(*args, **kw):
			with lock:
				return f(*args, **kw)

		return newFunction

	return wrap


# @log(logging.getLogger('main'), level='warning')
# logger
def log(logger, level = 'info'):
	def log_decorator(fn):
		@functools.wraps(fn)
		def wrapper(*a, **kwa):
			getattr(logger, level)(fn.__name__)
			return fn(*a, **kwa)

		return wrapper

	return log_decorator


def argtype(**decls):
	"""Decorator to check argument types.

	Usage:

	@argtype(name=str, text=str)
	def parse_rule(name, text): ...
	"""

	def decorator(func):
		code = func.__code__
		fname = func.__name__  # or func_name?
		names = code.co_varnames[:code.co_argcount]

		@functools.wraps(func)
		def decorated(*args, **kwargs):
			for argname, argtype in decls.iteritems():
				try:
					argval = args[names.index(argname)]
				except ValueError:
					argval = kwargs.get(argname)
				if argval is None:
					raise TypeError("%s(...): arg '%s' is null"
					                % (fname, argname))
				if not isinstance(argval, argtype):
					raise TypeError("%s(...): arg '%s': type is %s, must be %s"
					                % (fname, argname, type(argval), argtype))
			return func(*args, **kwargs)

		return decorated

	return decorator
