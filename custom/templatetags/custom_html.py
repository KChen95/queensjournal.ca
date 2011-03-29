import re
from django import template
from django.utils.encoding import smart_unicode
from htmlentitydefs import codepoint2name
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ungettext, ugettext
from datetime import datetime

register = template.Library()

def convert_entities(value):
	"""
	Better conversion method from Unicode to HTML entities.
	"""
	entities = list()
	for c in value:
		if ord(c) < 128:
			entities.append(c)
		else:
			try:
				entities.append('&%s;' % codepoint2name[ord(c)])
			except KeyError:
				continue
	return ''.join(entities)

def linebreakswithcode(value):
	"""
	Inserts paragraph tags at line breaks, EXCEPT when an HTML element starts the
	next line.
	"""
	INLINE_ELEMENTS = ['em','strong','q','cite','dfn','abbr','acronym',
					   'code','samp','kbd','var','sub','sup','del','ins','a',
					   'img','br','map','area','object','param','span']
	from django.utils.html import linebreaks
	inline_regex = '|'.join(INLINE_ELEMENTS)
	wrappedblockshtml_re = re.compile(r'(<p>|<br */>)+(<(?!' + inline_regex + ')([^>]*)>[^\r\n]+</\3>)(</p>|<br */>)+')
	trappedbreakshtml_re = re.compile(r'(</?(?!' + inline_regex + ')[^>]+>)<br */>(?=</?(?!' + inline_regex + ')[^>]+>)')
	value = linebreaks(value)
	value = wrappedblockshtml_re.sub(r'\2', value)
	value = trappedbreakshtml_re.sub(r'\1', value)
	return value

def stripspace(value):
	"""
	Strips leading and trailing whitespace. (Why isn't this already a standard
	Django filter? The mind boggles.)
	"""
	return value.strip()

def choptext(value, char='20'):
   count = int(char)
   if len(value) > count:
	  count = count - 1
	  exp = r'^\s*(.{0,%s}[^\s])\b\s*(.*)' % char
	  m = re.compile(exp).match(value)
	  result = '<span class="chopped">%s<span> %s</span></span>' % (conditional_escape(m.group(1)), conditional_escape(m.group(2)))
	  return mark_safe(result)
   else:
	  return value
	
def date_diff(timestamp, to=None):
	if not timestamp:
		return ""

	compare_with = to or datetime.now()
	delta = timestamp - compare_with

	if delta.days == 0: return u"today"
	elif delta.days == -1: return u"yesterday"
	elif delta.days == 1: return u"tomorrow"

	chunks = (
		(365.0, lambda n: ungettext('year', 'years', n)),
		(30.0, lambda n: ungettext('month', 'months', n)),
		(7.0, lambda n : ungettext('week', 'weeks', n)),
		(1.0, lambda n : ungettext('day', 'days', n)),
	)

	for i, (chunk, name) in enumerate(chunks):
		if abs(delta.days) >= chunk:
			count = abs(round(delta.days / chunk, 0))
			break

	date_str = ugettext('%(number)d %(type)s') % {'number': count, 'type': name(count)}

	if delta.days > 0: return "in " + date_str
	else: return date_str + " ago"

register.filter(convert_entities)
register.filter(linebreakswithcode)
register.filter(stripspace)
register.filter(choptext)
register.filter(date_diff)
