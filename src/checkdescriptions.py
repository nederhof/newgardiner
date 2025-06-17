import tkinter as tk

from unikemet import read_unikemet
from PIL import Image, ImageDraw, ImageFont, ImageTk

CHART_DIR = '../docs/glyphs16/'
FONT = '../fonts/NewGardiner.ttf'
UNIK = '../tables/Unikemet16revised.txt'
COMMENTS = 'comments.txt'

CANVAS_W = 256
CANVAS_H = 256
FONT_SIZE = 200

page_ranges = [
{'start': 0x13460}, {'start': 0x13560}, {'start': 0x13660}, {'start': 0x13760},
{'start': 0x13860}, {'start': 0x13960}, {'start': 0x13A60}, {'start': 0x13B60},
{'start': 0x13C60}, {'start': 0x13D60}, {'start': 0x13E60}, {'start': 0x13F50},
{'start': 0x14040}, {'start': 0x14130}, {'start': 0x14220}, {'start': 0x14310}, {'start': 0x143FB}]
PAGE = 15
FIRST = page_ranges[PAGE]['start']
LAST = page_ranges[PAGE+1]['start']-1

class DescriptionChecker:
	def __init__(self, root):
		self.root = root
		self.root.title('Description checker')
		self.descriptions = read_unikemet(UNIK)['desc']
		self.cores = read_unikemet(UNIK)['core']
		self.code_point = FIRST
		self.font = ImageFont.truetype(FONT, FONT_SIZE)

		self.chart_canvas = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H)
		self.chart_canvas.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

		self.font_canvas = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H)
		self.font_canvas.grid(row=2, column=0, rowspan=2, padx=10, pady=10)

		self.code_label = tk.Label(root, text='', wraplength=100, anchor='w', justify='left')
		self.code_label.grid(row=0, column=1, sticky='w', padx=(0, 10))

		self.desc_label = tk.Text(root, height=5, width=100, wrap='word')
		self.desc_label.grid(row=1, column=1, rowspan=2, sticky="w", padx=(0, 10))
		self.desc_label.config(state='disabled')

		self.comment_entry = tk.Text(root, height=5, width=40)
		self.comment_entry.grid(row=3, column=1, sticky='ew', padx=(0, 10), pady=5)
		self.comment_entry.bind('<Return>', self.on_enter)
		
		self.enter_btn = tk.Button(root, text='Enter', command=self.on_enter)
		self.enter_btn.grid(row=4, column=1, sticky='e', padx=(0, 10), pady=10)

		nav_frame = tk.Frame(root)
		nav_frame.grid(row=4, column=0, sticky='w', padx=10, pady=10)
		self.back_btn = tk.Button(nav_frame, text='Previous', command=self.go_to_prev)
		self.back_btn.pack(side='left')
		self.next_btn = tk.Button(nav_frame, text='Next', command=self.go_to_next)
		self.next_btn.pack(side='left', padx=(5,0))

		root.grid_columnconfigure(1, weight=1)

		self.show_glyph()

	def show_glyph(self):
		if self.code_point not in self.cores:
			self.go_to_next()
			return
		description = self.descriptions[self.code_point] if self.code_point in self.descriptions else ''

		self.code_label.config(text=f'U+{self.code_point:X}')

		chart_path = f'{CHART_DIR}{self.code_point}.png'
		chart_img = Image.open(chart_path).resize((CANVAS_W, CANVAS_H))
		self.chart_img_tk = ImageTk.PhotoImage(chart_img)
		self.chart_canvas.delete('all') 
		self.chart_canvas.create_image(CANVAS_W // 2, CANVAS_H // 2, image=self.chart_img_tk)

		self.desc_label.config(state='normal')
		self.desc_label.delete('1.0', 'end')
		self.desc_label.insert('1.0', description)
		self.desc_label.config(state='disabled')
		font_img = Image.new('RGBA', (CANVAS_W, CANVAS_H), (255, 255, 255, 0))
		draw = ImageDraw.Draw(font_img)
		try:
			c = chr(self.code_point)
		except ValueError:
			c = self.code_point
		bbox = draw.textbbox((0, 0), c, font=self.font)
		w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
		x = (CANVAS_W-w)//2
		y = (CANVAS_H-h)//2 - FONT_SIZE + h
		y = (CANVAS_H+h)//2 - FONT_SIZE
		draw.text((x, y), c, font=self.font, fill=(0,0,0,255))
		self.font_img_tk = ImageTk.PhotoImage(font_img)
		self.font_canvas.delete('all')
		self.font_canvas.create_image(CANVAS_W // 2, CANVAS_H // 2, image=self.font_img_tk)

		self.comment_entry.delete('1.0', 'end')
		self.comment_entry.yview_moveto(0)
		self.comment_entry.mark_set('insert', '1.0')
		self.comment_entry.focus_set()

	def on_enter(self, event=None):
		comment = self.comment_entry.get('1.0', 'end-1c').strip()
		if comment:
			with open(COMMENTS, 'a', newline='', encoding='utf-8') as f:
				f.write(f'0x{self.code_point:X}\n')
				f.write(f'{comment}\n\n')
		self.go_to_next()

	def go_to_next(self):
		if self.code_point < LAST:
			self.code_point = self.code_point + 1
			if self.code_point not in self.cores:
				self.go_to_next()
			else:
				self.show_glyph()
		else:
			self.root.destroy()

	def go_to_prev(self):
		if self.code_point > FIRST:
			self.code_point = self.code_point - 1
			if self.code_point not in self.cores:
				self.go_to_prev()
			else:
				self.show_glyph()
		else:
			self.root.destroy()

def open_window():
	window = Tk()
	label = Label(window)
	label.pack()
	canvas = Canvas(window, bg='white', width=400, height=400)
	canvas.pack()
	accept = Button(window, text='Classify', height=2, bg='green', fg='white',
		font=('bold', 30), command=classify_manual)
	accept.pack()

if __name__ == '__main__':
	root = tk.Tk()
	app = DescriptionChecker(root)
	root.mainloop()
