
__all__ = ["ValidationError"]

class ValidationError(Exception):
	def __init__(self, message="", **kwargs):
		self.message = message

	def __str__(self):
		return self.message

	def __repr__(self):
		return '%s(%s,)' % (self.__class__.__name__, self.message)
