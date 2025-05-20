# Use this script to join two fonts. Where a code point is defined in both fonts, 
# the glyph from the primary font is taken.
# However, font properties such as em size, ascent and descent are copied from
# the secondary font; this may need manual adjustment.
# Typical usage:
# (0) Install fontforge, e.g. with:
# pip install fontforge
# (1) Put the two font files to be joined in the same directory as this script.
# (2) Adjust the definitions of the names of fontfiles as below.
# (3) Run:
# python joinfonts.py

import fontforge

primary_filename = 'NewGardiner.ttf'
secondary_filename = 'BBAW-Schoell-regular.ttf'

joined_filename = 'NewGardiner-BBAW-Schoell.ttf'
joined_fontname = 'NewGardiner-BBAW-Schoell'

primary_font = fontforge.open(primary_filename)
secondary_font = fontforge.open(secondary_filename)

for glyph in primary_font.glyphs():
	code = glyph.unicode
	if code >= 0:
		primary_font.selection.select(("ranges", None), code, code)
		primary_font.copy()
		secondary_font.selection.select(("ranges", None), code, code)
		secondary_font.paste()

secondary_font.fontname = joined_fontname
secondary_font.familyname = joined_fontname
secondary_font.fullname = joined_fontname

secondary_font.generate(joined_filename)
