from lxml import etree
import os

NONCORE_FILE = '../tables/noncore.csv'
TARGET_DIR = '../docs/'

with open(NONCORE_FILE, 'r') as f:
	noncores = [int(line, 16) for line in f]

def page_filename(page_num):
	return f'page{page_num}.html'

def page_range(page_start, page_end):
	return f'{page_start:X}-{page_end-1:X}'

def generate_table(body, page_start, page_end):
	table = etree.SubElement(body, 'table')
	thead = etree.SubElement(table, 'thead')
	tr_header = etree.SubElement(thead, 'tr')
	etree.SubElement(tr_header, 'th', {'class': 'label'})
	num_columns = -(-(page_end - page_start) // 16)
	for col in range(num_columns):
		col_label = (page_start // 16) + col
		th = etree.SubElement(tr_header, 'th', {'class': 'label'})
		th.text = f'{col_label:X}x'
	tbody = etree.SubElement(table, 'tbody')
	num_rows = 16
	for row in range(num_rows):
		tr = etree.SubElement(tbody, 'tr')
		th_row = etree.SubElement(tr, 'td', {'class': 'label'})
		th_row.text = f'{row:X}'
		for col in range(num_columns):
			code_point = page_start + col * num_rows + row
			if code_point < page_end:
				td = etree.SubElement(tr, 'td')
				if code_point in noncores:
					div_noncore = etree.SubElement(td, 'div', {'class': 'noncore'})
					div_noncore.text = 'NC'
				else:
					div_glyph = etree.SubElement(td, 'div', {'class': 'glyph'})
					div_glyph.text = chr(code_point)
				div_code = etree.SubElement(td, 'div', {'class': 'code'})
				div_code.text = f'{code_point:X}'
			else:
				td = etree.SubElement(tr, 'td', {'class': 'unused'})

def generate_page(page_num, previous_page, next_page, page_start, page_end):
	html = etree.Element('html', lang='en')
	head = etree.SubElement(html, 'head')
	etree.SubElement(head, 'meta', charset='UTF-8')
	etree.SubElement(head, 'meta', name='viewport', content='width=device-width, initial-scale=1.0')
	title = etree.SubElement(head, 'title')
	title.text = 'NewGardiner ' + page_range(page_start, page_end)
	etree.SubElement(head, 'link', rel='stylesheet', href='style.css')
	body = etree.SubElement(html, 'body')
	h1 = etree.SubElement(body, 'h1')
	a = etree.SubElement(h1, 'a', {'href': 'index.html'})
	a.text = 'NewGardiner font'
	navigation = etree.SubElement(body, 'div', {'class': 'navigation'})
	if previous_page is not None:
		previous_button = etree.SubElement(navigation, 'a', {'href': page_filename(previous_page), 'class': 'button'})
		previous_button.text = '⬅'
	subtitle = etree.SubElement(navigation, 'span')
	subtitle.text = page_range(page_start, page_end)
	if next_page is not None:
		next_button = etree.SubElement(navigation, 'a', {'href': page_filename(next_page), 'class': 'button'})
		next_button.text = '➡'
	generate_table(body, page_start, page_end)
	html_string = etree.tostring(html, pretty_print=True, doctype='<!DOCTYPE html>', encoding='unicode')
	with open(TARGET_DIR + page_filename(page_num), 'w', encoding='utf-8') as f:
		f.write(html_string)

def generate_index(page_index):
	html = etree.Element('html', lang='en')
	head = etree.SubElement(html, 'head')
	etree.SubElement(head, 'meta', charset='UTF-8')
	etree.SubElement(head, 'meta', name='viewport', content='width=device-width, initial-scale=1.0')
	title = etree.SubElement(head, 'title')
	title.text = 'NewGardiner font'
	etree.SubElement(head, 'link', rel='stylesheet', href='style.css')
	body = etree.SubElement(html, 'body')
	h1 = etree.SubElement(body, 'h1')
	h1.text = 'NewGardiner font'
	download = etree.SubElement(body, 'h2')
	download.text = 'More information and download'
	download_par = etree.SubElement(body, 'p')
	download_link = etree.SubElement(download_par, 'a', {'href': 'https://github.com/nederhof/newgardiner'})
	download_link.text = 'on GitHub'
	charts = etree.SubElement(body, 'h2')
	charts.text = 'Charts'
	for page in page_index:
		page_par = etree.SubElement(body, 'p')
		page_link = etree.SubElement(page_par, 'a', {'href': page_filename(page['page_num'])})
		page_link.text = page_range(page['page_start'], page['page_end'])
	html_string = etree.tostring(html, pretty_print=True, doctype='<!DOCTYPE html>', encoding='unicode')
	with open(TARGET_DIR + 'index.html', 'w', encoding='utf-8') as f:
		f.write(html_string)

def generate_pages(page_ranges):
	page_index = []
	for page_num, page_range in enumerate(page_ranges):
		previous_page = page_num-1 if page_num > 0 else None
		next_page = page_num+1 if page_num < len(page_ranges) - 1 else None
		page_start = page_range['start']
		page_end = page_range['end'] if 'end' in page_range else page_ranges[page_num+1]['start']
		generate_page(page_num, previous_page, next_page, page_start, page_end)
		page_index.append({'page_num': page_num, 'page_start': page_start, 'page_end': page_end})
	generate_index(page_index)

page_ranges = [{'start': 0x13000}, {'start': 0x130E0}, {'start': 0x131C0}, {'start': 0x13290}, {'start': 0x13360, 'end': 0x13430},
{'start': 0x13460}, {'start': 0x13560}, {'start': 0x13660}, {'start': 0x13760},
{'start': 0x13860}, {'start': 0x13960}, {'start': 0x13A60}, {'start': 0x13B60},
{'start': 0x13C60}, {'start': 0x13D60}, {'start': 0x13E60}, {'start': 0x13F50},
{'start': 0x14040}, {'start': 0x14130}, {'start': 0x14220}, {'start': 0x14310, 'end': 0x143FB}]

generate_pages(page_ranges)
