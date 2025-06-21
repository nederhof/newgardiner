from lxml import etree
import os
import copy

from unikemet import read_unikemet

ERR_SOURCE = '../tables/unicode5to16err.txt'
DIFF_SOURCE = '../tables/unicode5to16diff.txt'
PREFIX = '../tables/corruptionprefix.html'
TARGET_DIR = '../docs/'
TARGET_FILE = TARGET_DIR + 'unicode5to16corruption.html'
STAND_ALONE_FILE = TARGET_DIR + 'standalonecorruption.html'
DIR5 = 'glyphs5'
DIR16 = 'glyphs16'

def read_item(lines):
	first_parts = lines[0].split()
	ok = False
	if first_parts[0] == 'ok':
		first_parts = first_parts[1:]
		ok = True
	code_points = [int(h, 16) for h in first_parts]
	return {'code_point': code_points[0], \
			'others': code_points[1:], \
			'comment_pars': ''.join(lines[1:]).split('<p>'),
			'ok': ok}

def read_diff_file(path):
	items = []
	with open(path, 'r') as f:
		lines = []
		for line in f:
			if line.strip() == '':
				if len(lines) > 0:
					items.append(read_item(lines))
				lines = []
			else:
				lines.append(line)
		if len(lines) > 0:
			items.append(read_item(lines))
	return items

def desc_string(tables, code_point):
	if code_point in tables['desc']:
		desc = tables['desc'][code_point]
		return f'U+{code_point:X} kEH_Desc {desc}'
	else:
		return None

def may_attach_desc_string(elem, tables, code_point, br=False):
	desc = desc_string(tables, code_point)
	if desc is not None:
		if br:
			etree.SubElement(elem, 'br')
		tt = etree.SubElement(elem, 'tt')
		tt.text = desc

def attach_image5(elem, code_point, code_points):
	etree.SubElement(elem, 'img', {'src': f'{DIR5}/{code_point}.png', 'class': 'image5'})
	code_points.add(code_point)

def attach_image16(elem, code_point, code_points):
	etree.SubElement(elem, 'img', {'src': f'{DIR16}/{code_point}.png', 'class': 'image16'})
	code_points.add(code_point)

def make_difference(body, diff, tables, code_points):
	code_point = diff['code_point']
	others = diff['others']
	comment_pars = diff['comment_pars']
	ok = diff['ok']
	table = etree.SubElement(body, 'table', {'class': 'glyph_table'})
	tbody = etree.SubElement(table, 'tbody')
	tr = etree.SubElement(tbody, 'tr')
	td = etree.SubElement(tr, 'td')
	attach_image5(td, code_point, code_points)
	attach_image16(td, code_point, code_points)
	div_code = etree.SubElement(td, 'div', {'class': 'code'})
	div_code.text = f'{code_point:X}'
	for other in others:
		td_other = etree.SubElement(tr, 'td')
		attach_image16(td_other, other, code_points)
		div_other = etree.SubElement(td_other, 'div', {'class': 'code'})
		div_other.text = f'{other:X}'
	p_desc = etree.SubElement(body, 'p')
	may_attach_desc_string(p_desc, tables, code_point)
	for other in others:
		may_attach_desc_string(p_desc, tables, other, br=True)
	for comment_par in comment_pars:
		comment_par = comment_par.strip()
		if ok:
			par = etree.SubElement(body, 'p', {'class': 'done'})
		else:
			par = etree.SubElement(body, 'p')
		if comment_par.startswith('http'):
			a = etree.SubElement(par, 'a', {'href': comment_par})
			a.text = comment_par
		else:
			par.text = comment_par.replace('0x', 'U+')

def make_page(tables):
	html = etree.Element('html', lang='en')
	head = etree.SubElement(html, 'head')
	etree.SubElement(head, 'meta', charset='UTF-8')
	etree.SubElement(head, 'meta', name='viewport', content='width=device-width, initial-scale=1.0')
	title = etree.SubElement(head, 'title')
	title.text = 'Differences Unicode 5.2 / Unicode 16'
	etree.SubElement(head, 'link', rel='stylesheet', href='style.css')
	body = etree.SubElement(html, 'body')
	h1 = etree.SubElement(body, 'h1')
	h1.text = title.text
	p = etree.SubElement(body, 'p')
	p.text = 'Where two glyphs are given for the same code point, the first is from Unicode 5.2 and the second is from Unicode 16. The glyphs were automatically extracted from the official PDF code charts. Lines in blue starting with code point and kEH_Desc are descriptions copied verbatim from Unikemet. Comments in green indicate that the issues were resolved.'
	h2 = etree.SubElement(body, 'h2')
	h2.text = 'Apparent errors'
	code_points = set()
	errata = read_diff_file(ERR_SOURCE)
	for erratum in errata:
		make_difference(body, erratum, tables, code_points)
	h2 = etree.SubElement(body, 'h2')
	h2.text = 'Other noteworthy differences (maybe not errors?)'
	differences = read_diff_file(DIFF_SOURCE)
	for diff in differences:
		make_difference(body, diff, tables, code_points)
	return html, code_points

def make_standalone_page(tables):
	html, code_points = make_page(tables)
	first_h1 = html.find('.//h1')
	first_p = html.find('.//p')
	first_h1.getparent().remove(first_h1)
	first_p.getparent().remove(first_p)
	with open(PREFIX, 'r') as f:
		prefix_tree = etree.HTML(f.read())
	prefix_elems = prefix_tree.find('.//body')
	target_body = html.find('.//body')
	for elem in reversed(list(prefix_elems)):
		target_body.insert(0, copy.deepcopy(elem))
	return html, code_points


def write_page(tables):
	html, _ = make_page(tables)
	html_string = etree.tostring(html, pretty_print=True, doctype='<!DOCTYPE html>', encoding='unicode')
	with open(TARGET_FILE, 'w', encoding='utf-8') as f:
		f.write(html_string)

def write_standalone_page(tables):
	html, _ = make_standalone_page(tables)
	html_string = etree.tostring(html, pretty_print=True, doctype='<!DOCTYPE html>', encoding='unicode')
	with open(STAND_ALONE_FILE, 'w', encoding='utf-8') as f:
		f.write(html_string)

if __name__ == '__main__':
	tables = read_unikemet('../tables/Unikemet-16.0.0.txt')
	write_page(tables)
	write_standalone_page(tables)
