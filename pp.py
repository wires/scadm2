import json, pygments

def pp(obj):
	"""Pretty print an object"""

	from pygments import highlight
	from pygments.lexers import JsonLexer
	from pygments.formatters import TerminalFormatter

	s = json.dumps(obj, indent=2, sort_keys=True)

	print highlight(s, JsonLexer(), TerminalFormatter())
