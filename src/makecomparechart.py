from lxml import etree
import os

TARGET_DIR = '../docs/'
BASE_NAME = 'unicode5to16compare'
DIR5 = 'glyphs5'
DIR16 = 'glyphs16'

def index_filename():
	return f'{BASE_NAME}.html'

def index_path():
	return f'{TARGET_DIR}{index_filename()}'

def page_filename(page_num):
	return f'{BASE_NAME}{page_num}.html'

def page_path(page_num):
	return f'{TARGET_DIR}{page_filename(page_num)}'

def image_path5(code_point):
	return f'{DIR5}/{code_point}.png'

def image_path16(code_point):
	return f'{DIR16}/{code_point}.png'

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
				etree.SubElement(td, 'img', {'src': image_path5(code_point), 'class': 'image5'})
				etree.SubElement(td, 'img', {'src': image_path16(code_point), 'class': 'image16'})
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
	title.text = f'Unicode 5.2 versus Unicode 16 {page_start:X}-{page_end:X}'
	etree.SubElement(head, 'link', rel='stylesheet', href='style.css')
	body = etree.SubElement(html, 'body')
	h1 = etree.SubElement(body, 'h1')
	a = etree.SubElement(h1, 'a', {'href': index_filename()})
	a.text = 'Unicode 5.2 versus Unicode 16'
	navigation = etree.SubElement(body, 'div', {'class': 'navigation'})
	if previous_page is not None:
		previous_button = etree.SubElement(navigation, 'a', {'href': page_filename(previous_page), 'class': 'button'})
		previous_button.text = '⬅'
	subtitle = etree.SubElement(navigation, 'span')
	subtitle.text = f'{page_start:X}-{page_end:X}'
	if next_page is not None:
		next_button = etree.SubElement(navigation, 'a', {'href': page_filename(next_page), 'class': 'button'})
		next_button.text = '➡'
	generate_table(body, page_start, page_end)
	html_string = etree.tostring(html, pretty_print=True, doctype='<!DOCTYPE html>', encoding='unicode')
	with open(page_path(page_num), 'w', encoding='utf-8') as f:
		f.write(html_string)

def generate_index(page_index):
	html = etree.Element('html', lang='en')
	head = etree.SubElement(html, 'head')
	etree.SubElement(head, 'meta', charset='UTF-8')
	etree.SubElement(head, 'meta', name='viewport', content='width=device-width, initial-scale=1.0')
	title = etree.SubElement(head, 'title')
	title.text = 'Unicode 5.2 versus Unicode 16'
	etree.SubElement(head, 'link', rel='stylesheet', href='style.css')
	body = etree.SubElement(html, 'body')
	h1 = etree.SubElement(body, 'h1')
	h1.text = 'Unicode 5.2 versus Unicode 16'
	for page in page_index:
		page_par = etree.SubElement(body, 'p')
		page_link = etree.SubElement(page_par, 'a', {'href': page_filename(page['page_num'])})
		page_link.text = f'{page['page_start']:X}-{page['page_end']:X}'
	html_string = etree.tostring(html, pretty_print=True, doctype='<!DOCTYPE html>', encoding='unicode')
	with open(index_path(), 'w', encoding='utf-8') as f:
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

page_ranges = [{'start': 0x13000}, {'start': 0x130E0}, {'start': 0x131C0}, {'start': 0x13290}, {'start': 0x13360, 'end': 0x1342F}]

generate_pages(page_ranges)
