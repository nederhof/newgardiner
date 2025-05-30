from lxml import etree
import os

from unikemet import read_unikemet

TARGET_DIR = '../docs/'
TARGET_FILE = TARGET_DIR + 'unicode5to16corruption.html'
DIR5 = 'glyphs5'
DIR16 = 'glyphs16'

errata = \
[
{'code_point': 0x13017, 'others': [0x134CD],
'comment': 'The staff in the original shape of 0x13017 already had a slight backward angle, unlike the Unicode 16 form, where the staff is perfectly vertical. This will be solved in Unicode 17 by redrawing 0x13017 to have the staff at a backward angle, like in the original shape. But note that then 0x13017 and 0x134CD will differ by no more than the exact degree of the angle, which seems an inappropriately small graphical distinction for the purposes of Unicode.'},
{'code_point': 0x1303A, 'others': [0x1355D],
'comment': 'Considering the hairstyles, 0x1303A was misplaced at 0x1355D. This will be solved in Unicode 17 by swapping the shapes and ancillary documention of 0x1303A and 0x1355D from Unicode 16.'},
{'code_point': 0x130C1, 'others': [],
'comment': 'These are arguably only insignificant graphical variants of the same thing, but unless one can argue that one variant is real and the other variant is not real (never occurs), one should revert to the original Unicode 5.2 variant, and change description and image accordingly. Incidentally, both forms exist in GEG. Around 2009, there were discussions about which of the two was the most appropriate form for Unicode, and in consultation with Egyptologists it was decided to opt for the form in Unicode 5.2. Whether or not you agree this was the right decision should be irrelevant. Code charts should not be changed without a compelling reason.'},
{'code_point': 0x130F9, 'others': [0x13ABE],
'comment': 'The original shape of 0x130F9 unmistakably had whiskers. This will be solved in Unicode 17 by swapping the shapes and ancillary documention of 0x130F9 and 0x13ABE from Unicode 16.'},
{'code_point': 0x130FA, 'others': [],
'comment': 'In the original shape, the hare has whiskers. Moreover, the difference between 0x130FA and 0x130F9 should be in the height, while the width should be roughly the same, i.e. 0x130FA is flatter than 0x130F9. See Gardiner (1957) for the typographical motivation. Both issues will be solved in Unicode 17.'},
{'code_point': 0x130FB, 'others': [0x13AE8],
'comment': 'The original shape (tail up) was misplaced at 0x13AE8. This will be solved in Unicode 17 by swapping the shapes and ancillary documention of 0x130FB and 0x13AE8 from Unicode 16.'},
{'code_point': 0x130FC, 'others': [],
'comment': 'The original shape had the tail up. This will be solved in Unicode 17 by restoring the orientation of the tail.'},
{'code_point': 0x13108, 'others': [0x13B83], 'comment': 'The original shape was misplaced at 0x13B83. The only reasonable solution is to swap shapes and ancillary documention from Unicode 16.'},
{'code_point': 0x13110, 'others': [], 'comment': 'Even though these are insignificant graphical variants, code charts should not be changed without a good reason. Unless a compelling case can be made that the horn over the liquid cannot occur in real inscriptions, revert to the Unicode 5.2 form.'},
{'code_point': 0x13112, 'others': [0x13BB2], 'comment': 'The appearance of 0x13112 has changed considerably and one could even argue that 0x13BB2 is closer to the original shape than to the new shape; both the original shape and 0x13BB2 clearly have sharp teeth while the new shape of 0x13112 does not. Gardiner (1957) characterizes the sign as "lower jaw-bone of ox", and as far as I know, oxen are not particularly known for having sharp teeth. But does this necessarily mean that the original shape of 0x13112 and 0x13BB2 differ in what they are meant to represent? Unless there is solid evidence that the original shape of 0x13112 was wrong or uncharacteristic, it may be better to revert the shape to something closer to Unicode 5.2. It is then an open question whether the current shape of 0x13BB2 deserves its own (core) code point.'},
{'code_point': 0x1315D, 'others': [0x13C5D], 'comment': 'The description of 0x1315D does not match the images. The original shape has a standard closer to R92A. So if a graphical variant is needed with R12, then it should be at a new code point, so here that would be 0x13C5D. In other words, flip the ancillary documentation and give 0x13C5D the R12 shape. Unicode 17 will regrettably have this the wrong way around. I hope this can be corrected in Unicode 18.'},
{'code_point': 0x13163, 'others': [0x13C4A], 'comment': 'It is by no more than a few black pixels, but it is unmistakable that the original shape was meant to exhibit a lappet. In other words, the shape of 0x13163 was misplaced at 0x13C4A. The only reasonable solution is to swap shapes and ancillary documention from Unicode 16.'},
{'code_point': 0x13164, 'others': [], 'comment': 'Give the shape a lappet to revert to Unicode 5.2.'},
{'code_point': 0x13169, 'others': [0x13168], 'comment': 'The width of 0x13169 should be the same as that of 0x13168, but the height should be smaller. See Gardiner (1957) for the typographical motivation. This will be corrected in Unicode 17.'},
{'code_point': 0x1316B, 'others': [0x1316A], 'comment': 'The width of 0x1316B should be the same as that of 0x1316A, but the height should be smaller. See Gardiner (1957) for the typographical motivation. This will be corrected in Unicode 17.'},
{'code_point': 0x131A6, 'others': [],
'comment': 'Around 2009, there were protracted discussions about what the most appropriate orientation was for Unicode, since both orientations occur in GEG, and the sign was taken from iconography and is not attested in actual running text. In consultation with Egyptologists it was decided to opt for the form in Unicode 5.2. Whether or not you agree this was the right decision at the time, having studied (or not) the arguments laid out by Egyptologists in 2009, all this should be irrelevant. The glyph should not change on a whim relative to what it has been for the past 15 years since Unicode 5.2. If anyone feels a need for the other orientation, a variation selector for rotation can be used.'},
{'code_point': 0x131C6, 'others': [], 'comment': 'Revert to the shape from Unicode 5.2. The description in fact already correctly reflects the original shape.'},
{'code_point': 0x131D8, 'others': [], 'comment': 'It is unclear which sign is on top in Unicode 5.2, so fonts have the liberty to interpret this as desired, but at least make sure the shape is consistent with the description, which is currently not the case.'},
{'code_point': 0x131F4, 'others': [0x131F6, 0x13EDE, 0x13EDF, 0x13EE0], 'comment': 'There is no inner circle in the original shape of 0x131F4. One may argue this is an insignificant detail. But if one then introduces multiple code points 0x131F6 and 0x13EDE for the same sign with and without inner circle, and similarly 0x13EDF and 0x13EE0, then one simultaneously suggests that the inner circle is important and that the inner circle is not important. See also the Guidelines, which more often than not are divorced from what was actually done.'},
{'code_point': 0x13227, 'others': [], 'comment': 'The differences may be insignificant, but it appears to me that most of the description matches the original shape better than the Unicode 16 shape, in particular the orientation of the feather and the "short vertical line". This sign deserves to be revisited by an expert'},
{'code_point': 0x13228, 'others': [], 'comment': 'I think the description matches the spear better in the original shape than in the Unicode 16 shape. This sign deserves to be revisited by an expert.'},
{'code_point': 0x13246, 'others': [], 'comment': 'The Unicode 16 form does not seem to match the description, because it does not appear to have the usual R12 standard, as it does in the original. Also, in the original, the hare has whiskers.'},
{'code_point': 0x1324A, 'others': [], 'comment': 'This does not remotely seem to be the same character. Even if the original shape is wrong, in the sense of being a misinterpretation of actual inscriptions, the new shape would have deserved a new code point, rather than trying to recycle an existing code point for a totally different thing. It is a mystery to me where the current shape comes from; it has been in the code charts since at least Unicode 9.'},
{'code_point': 0x1326E, 'others': [], 'comment': 'The description of the shape of the roof matches the original shape but not the new shape.'},
{'code_point': 0x13271, 'others': [], 'comment': 'In the original, the sides were more oblique than vertical.'},
{'code_point': 0x13277, 'others': [0x13FDC], 'comment': 'The original shape (without circle) was misplaced at 0x13FDC. The only reasonable solution is to swap shapes and ancillary documention from Unicode 16.'},
{'code_point': 0x1329F, 'others': [], 'comment': 'The new shape is mirrored. Since there is a mirroring control, there is no reasonable justification for this, even if the sign normally occurs the other way around.'},
{'code_point': 0x132BC, 'others': [0x14107], 'comment': 'The original shape of 0x132BC was misplaced at 0x14107. The only reasonable solution is to swap shapes and ancillary documention from Unicode 16.'},
{'code_point': 0x132F6, 'others': [], 'comment': 'The description matches the original shape but not the new shape. In the new shape the piece of cloth is over the sickle.'},
{'code_point': 0x1330C, 'others': [], 'comment': 'The original shape underspecified which of the signs is on top. It seems fine to me to clarify the desired appearance, if there is a sufficient amount of evidence suggesting that one or the other form is correct. But the new shape should be consistent with the description. In the new shape, the cobra is under the mace.'},
{'code_point': 0x1330D, 'others': [], 'comment': 'The description matches the original shape but not the new shape. In the new shape the mace is over the cobras.'},
{'code_point': 0x1331C, 'others': [0x131C5, 0x131D5], 'comment': 'In the original code charts, the handle most certainly does not resemble M13 (0x131C5), If anything, it looks closer to 0x131D5.  I do not mind if the image in the code charts currently has that shape, as the shape of the handle seems a minor detail. But by putting "with a handle resembling ..." in the description you suggest that M13 is an essential part of the character identity of 0x1331C, whereas (as far as I know) scimitars do not generally have a handle resembling M13. The Database does not motivate departing from the original shape. The TSL has one single token (without citation!), which is rather blurry and does not seem to suggest M13 at all.'},
{'code_point': 0x1332F, 'others': [], 'comment': 'By plausible deniability one could argue the new shape underspecifies which sign is on top. But in Unicode 16, the shapes of overlays generally commit to one or the other. It would be better therefore to revert to the Unicode 5.2 shape.'},
{'code_point': 0x13332, 'others': [], 'comment': 'The original shape did not have a boss. It is fine to improve the appearance. But the new shape and the description do not seem to match. In the new shape, the boss is not really "in the center".'},
{'code_point': 0x13341, 'others': [0x1429C], 'comment': 'It is unclear to me whether the original shape of 0x13341 is closer to its new shape, or whether it rather corresponds to 0x1429C. The original shape had a pronounced circle, like 0x1429C, while the new shape has more of a bulb. Does it even make sense to have two code points here?'},
{'code_point': 0x1334C, 'others': [0x1334B, 0x142B7, 0x142B8], 'comment': 'The original shape of 0x1334C has a horizontal line on the top, so the new shape is wrong. The intended use of 0x1334C is for "a later form of U23" (Gardiner 1931) as found on the 26th Dyn. sarcophagus of Ankhnesneferibra (BM EA32). See the bottom-left corner of the image in the link below, where it reads at the end of the column "n mr=s n [...]"; there is most definitely a line on the top. The Database refers to the Pyramid of Unas, which is off by 2 millennia so this is unlikely to be relevant to 0x1334C. It is unclear to me how other newly introduced code points for hair-pins are supposed to relate to the original shape of 0x1334C, or even how to characterize the difference between 0x1334C and usual hairpin 0x1334B. It becomes an exercise in futility if new code points are introduced for barely distinguishable shapes, as if those are meaningful for Unicode, while the intentions of existing code points are distorted to turn them into totally different things. One either takes the character identities of code points seriously, or one does not, in which case why do we even bother with Unicode?',
'url': 'https://www.britishmuseum.org/collection/object/Y_EA32?selectedImageId=1495613001'},
{'code_point': 0x1335A, 'others': [], 'comment': 'Apart from plausible deniability (see above), the description matches the original shape but not the new shape. In the new shape the spindle is over the viper.'},
{'code_point': 0x13393, 'others': [], 'comment': 'Apart from plausible deniability (see above), the description matches the original shape but not the new shape. It would be better to revert to the Unicode 5.2 shape.'},
{'code_point': 0x1339C, 'others': [], 'comment': 'Apart from plausible deniability (see above), the new shape, unlike the description, suggests the wick is over the arm. Make the new shape consistent with the description.'},
{'code_point': 0x1339E, 'others': [], 'comment': 'Even though these are insignificant graphical variants, code charts should not be changed without a good reason. Unless a compelling case can be made that the basket over the hank of fibre cannot occur in real inscriptions, revert to the Unicode 5.2 form.'},
{'code_point': 0x1341B, 'others': [], 'comment': 'The description matches the original shape but not the new shape. Correct the new shape to have the top line curve downwards.'},
{'code_point': 0x13424, 'others': [], 'comment': 'Apart from plausible deniability (see above), the new shape, unlike the description, suggests the object is over the arm. Make the new shape consistent with the description.'},
{'code_point': 0x13427, 'others': [], 'comment': 'Even though these are insignificant graphical variants, code charts should not be changed without a good reason. Unless a compelling case can be made that the "thin triangle" over the moon cannot occur in real inscriptions, revert to the Unicode 5.2 form.'},
]

differences = \
[
{'code_point': 0x13043, 'others': [0x1333C],
'comment': 'In 0x13043, there was a line representing the ground, and there was no connecting rope. Now there is no line for the ground and there is a rope connecting the two pieces of the hoe. There may be good reasons to update the glyph, provided one can argue that the original form was incorrect. But there is a sign 0x1333C for a hoe without connecting rope, so the original glyph of 0x13043 is not implausible. If so far no token of 0x13043 was located without connecting rope, then what are you going to do if you do find such a token, introduce a new code point for it? This is disastrous for the stability of Unicode.'},
{'code_point': 0x1304F, 'others': [],
'comment': 'Hands were oriented outward, now inward. This may be a legitimate improvement since it has been argued that the shape with outward handpalms was plain wrong and does not occur in real inscriptions.'},
{'code_point': 0x13055 , 'others': [], 'comment': 'In the original shape, the hair is not long'},
{'code_point': 0x13057, 'others': [0x136D7, 0x136D9],
'comment': 'For 0x13057, there was a uraeus in the original, now there is not. There may be good reasons to update the glyph of 0x13057, provided one can argue the original shape was incorrect. But considering 0x136D7 and 0x136D9, which do have uraei, is it not plausible that the original shape might exist? If so far no token of 0x13057 was located with uraeus, then what are you going to do if you do find such a token, introduce a new code point for it? This is disastrous for the stability of Unicode.'},
{'code_point': 0x1306F, 'others': [0x1375D], 'comment': 'For 0x1306F, the sun-disk was removed. This is fine if the sun-disk in the original shape seems to have been due to a misinterpretation of known tokens. But note that there are headdresses in similar signs like 0x1375D with sun-disk.'},
{'code_point': 0x130B9, 'others': [], 'comment': 'It is debatable whether the original shape has the folded piece of cloth on top, or whether the intention was to underspecify which of the two signs is on top. In the latter case, it may be adequate to describe this simply as an overlay of the two signs without specifying which of the two is on top, and leave it to the font designer how to draw this. There are several more such cases.'},
{'code_point': 0x130E8, 'others': [], 'comment': 'The Unicode 5.2 form did not have the uraeus. If the missing uraeus was clearly a mistake, then fine. But if there is a reasonable chance one could also find occurrences without uraeus, will you then introduce a new code point for this once this happens? This is disastrous for the stability of Unicode.'},
{'code_point': 0x130F3, 'others': [], 'comment': 'Unicode 5.2 form did not have the four pieces of grain or fruit. Seems insignificant detail and one could just mention in the description that there is a basket without specifying what is in it.'},
{'code_point': 0x13146, 'others': [0x13C7C], 'comment': 'It is unclear to me what kind of standard was intended with the original shape of 0x13146, and it seems an insignificant detail. But if one starts introducing multiple code points depending on the choice of standard (cf. 0x13C7C), then it is not clear to me that the change of shape of 0x13146 is within the normal bounds of allowable graphical variation for a given code point, and perhaps a fresh code point would have been warranted.'},
{'code_point': 0x1314B, 'others': [], 'comment': 'The head of antilope was not previously discernible. Are *two* rudders visible, in both images?'},
{'code_point': 0x1314F , 'others': [0x137B8], 'comment': 'For 0x1314F, the sun-disk was removed. This is fine if the sun-disk in the original shape seems to have been due to a misinterpretation of known tokens. But note that there are headdresses in similar signs like 0x137B8 that do have a sun-disk.'},
{'code_point': 0x13233, 'others': [], 'comment': 'Child was given white crown. Bovid lost its horns.'},
{'code_point': 0x13234, 'others': [], 'comment': 'Child was given white crown.'},
{'code_point': 0x13235, 'others': [], 'comment': 'Headdress lost the sun-disk.'},
{'code_point': 0x13236, 'others': [], 'comment': 'The bow was mirrored.'},
{'code_point': 0x1323C, 'others': [], 'comment': 'The object on the standard changed from looking similar to Y8 to something closer to R28.'},
{'code_point': 0x13241, 'others': [], 'comment': 'In the original, the standard was simplified.'},
{'code_point': 0x13242, 'others': [], 'comment': 'In the original, the standard was simplified.'},
{'code_point': 0x13247, 'others': [], 'comment': 'There was no basket in the original shape. I understand the information in the Database to suggest this sign also occurs without basket. It might therefore have been better to keep the sign unchanged, as the original form is not objectively wrong.'},
{'code_point': 0x1324F, 'others': [], 'comment': 'Object on standard changed to a kind of overlay.'},
{'code_point': 0x1325F, 'others': [], 'comment': 'The original shape underspecified which of the signs is on top. It seems fine to me to clarify the desired appearance as is done here.'},
{'code_point': 0x1327F, 'others': [], 'comment': 'The original shape was asymmetric, while the new shape is perfectly symmetric. Can that be correct? I imagine a tenoned door not to be symmetric.'},
{'code_point': 0x1328F, 'others': [], 'comment': 'There was no loop at the front in the original.'},
{'code_point': 0x132BA, 'others': [], 'comment': 'The two shapes are similar. But I cannot relate the description to the shapes. What is the loop at the back?'},
{'code_point': 0x132BF, 'others': [], 'comment': 'The standard has a different shape.'},
{'code_point': 0x132C5, 'others': [], 'comment': 'There appears to be a sun-disk on the headdress in the original.'},
{'code_point': 0x132E1, 'others': [], 'comment': 'The original shape underspecified which of the signs is on top. It seems fine to me to clarify the desired appearance as is done here. One worry for this case and for related cases is this: if the description mentioning which sign is on top is based on just one occurrence, and if in fact both possibilities exist, then the description is unduly specific. It would then be better to simply say that this is an overlay without specifying which sign is on top.'},
{'code_point': 0x132F7, 'others': [], 'comment': 'In the original, the fringes are not sloping.'},
]

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
	comment = diff['comment']
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
	p_comment = etree.SubElement(body, 'p')
	p_comment.text = comment.replace('0x', 'U+')
	if 'url' in diff:
		p_link = etree.SubElement(body, 'a', {'href': diff['url']})
		p_link.text = 'Link'

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
	p.text = 'Where two glyphs are given for the same code point, the first is from Unicode 5.2 and the second is from Unicode 16. The glyphs were automatically extracted from the official PDF code charts. Lines in blue starting with code point and kEH_Desc are descriptions copied verbatim from Unikemet.'
	h2 = etree.SubElement(body, 'h2')
	h2.text = 'Apparent errors'
	code_points = set()
	for erratum in errata:
		make_difference(body, erratum, tables, code_points)
	h2 = etree.SubElement(body, 'h2')
	h2.text = 'Other noteworthy differences (maybe not errors?)'
	for diff in differences:
		make_difference(body, diff, tables, code_points)
	html_string = etree.tostring(html, pretty_print=True, doctype='<!DOCTYPE html>', encoding='unicode')
	with open(TARGET_FILE, 'w', encoding='utf-8') as f:
		f.write(html_string)
	return code_points

if __name__ == '__main__':
	tables = read_unikemet('../tables/Unikemet-16.0.0.txt')
	make_page(tables)
