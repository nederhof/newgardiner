from lxml import etree
import os

from unikemet import read_unikemet

SOURCE_DIR = '../tables/'
TARGET_DIR = '../docs/'
TARGET_FILE = TARGET_DIR + 'unicode16comments.html'
DIR5 = 'glyphs5'
DIR16 = 'glyphs16'

FIRST_EXTENDED = 0x13460

def read_comment(lines):
	first_parts = lines[0].split()
	ok = False
	if first_parts[0] == 'ok':
		first_parts = first_parts[1:]
		ok = True
	code_points = [int(h, 16) for h in first_parts]
	comment_pars = ''.join(lines[1:]).split('<p>')
	return {'code_points': code_points, 
			'comment_pars': comment_pars,
			'ok': ok}

def read_comment_page(source):
	comments = []
	with open(source, 'r') as f:
		lines = []
		for line in f:
			if line.strip() == '':
				if len(lines) > 0:
					comments.append(read_comment(lines))
					lines = []
			else:
				lines.append(line)
		if len(lines) > 0:
			comments.append(read_comment(lines))
	return comments

def read_comment_pages():
	comment_pages = []
	for num in range(16):
		source = f'{SOURCE_DIR}unicode16page{num}.txt'
		if os.path.isfile(source):
			comments = read_comment_page(source)
			comment_pages.append({'num': num+1, 'comments': comments})
	return comment_pages

def attach_image5(elem, code_point, code_points):
	etree.SubElement(elem, 'img', {'src': f'{DIR5}/{code_point}.png', 'class': 'image5'})
	code_points.add(code_point)

def attach_image16(elem, code_point, code_points):
	etree.SubElement(elem, 'img', {'src': f'{DIR16}/{code_point}.png', 'class': 'image16'})
	code_points.add(code_point)

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

def make_comment(body, comment, tables, code_points):
	comment_code_points = comment['code_points']
	comment_pars = comment['comment_pars']
	comment_ok = comment['ok']
	table = etree.SubElement(body, 'table', {'class': 'glyph_table'})
	tbody = etree.SubElement(table, 'tbody')
	tr = etree.SubElement(tbody, 'tr')
	for code_point in comment_code_points:
		td = etree.SubElement(tr, 'td')
		if code_point < FIRST_EXTENDED:
			attach_image5(td, code_point, code_points)
		else:
			attach_image16(td, code_point, code_points)
		div_code = etree.SubElement(td, 'div', {'class': 'code'})
		if code_point < FIRST_EXTENDED:
			div_code.text = f'{code_point:X} (5.2)'
		else:
			div_code.text = f'{code_point:X}'
	p_desc = etree.SubElement(body, 'p')
	for i, code_point in enumerate(comment_code_points):
		if i == 0:
			may_attach_desc_string(p_desc, tables, code_point)
		else:
			may_attach_desc_string(p_desc, tables, code_point, br=True)
	for comment_par in comment_pars:
		if comment_ok:
			par = etree.SubElement(body, 'p', {'class': 'done'})
		else:
			par = etree.SubElement(body, 'p')
		if comment_par.strip().startswith('http'):
			a = etree.SubElement(par, 'a', {'href': comment_par.strip()})
			a.text = comment_par.strip()
		else:
			par.text = comment_par.replace('0x', 'U+')

def make_page(comment_pages, tables):
	html = etree.Element('html', lang='en')
	head = etree.SubElement(html, 'head')
	etree.SubElement(head, 'meta', charset='UTF-8')
	etree.SubElement(head, 'meta', name='viewport', content='width=device-width, initial-scale=1.0')
	title = etree.SubElement(head, 'title')
	title.text = 'Comments on the extended list in Unicode 16'
	etree.SubElement(head, 'link', rel='stylesheet', href='style.css')
	body = etree.SubElement(html, 'body')
	h1 = etree.SubElement(body, 'h1')
	h1.text = title.text
	p = etree.SubElement(body, 'p')
	p.text = 'The glyphs of the extended list were automatically extracted from the official PDF code charts of Unicode 16. For the basic list, the glyphs are from the code charts of Unicode 5.2. Lines in blue starting with code point and kEH_Desc are descriptions copied verbatim from Unikemet. Comments in green indicate that the issues were resolved.'
	copyr = etree.SubElement(body, 'p')
	copyr.text = 'Glyphs are Copyright © 1991-2025 Unicode, Inc.'
	code_points = set()
	for comment_page in comment_pages:
		h2 = etree.SubElement(body, 'h2')
		h2.text = f'Page {comment_page["num"]}'
		for comment in comment_page['comments']:
			make_comment(body, comment, tables, code_points)
	html_string = etree.tostring(html, pretty_print=True, doctype='<!DOCTYPE html>', encoding='unicode')
	with open(TARGET_FILE, 'w', encoding='utf-8') as f:
		f.write(html_string)
	return code_points

if __name__ == '__main__':
	tables = read_unikemet('../tables/Unikemet-16.0.0.txt')
	comment_pages = read_comment_pages()
	make_page(comment_pages, tables)
