# NewGardiner font of Egyptian Hieroglyphs

This TrueType font was created at the [University of St Andrews](https://www.st-andrews.ac.uk/)
using [FontForge](https://fontforge.org/en-US/).
It is released under the SIL OFL 1.1 license.

It includes:

- All 1071 hieroglyphic signs introduced in Unicode 5.2 (2009). This is also referred to as the **basic list**.
- One additional sign introduced in Unicode 12 (2019).
- Most of the 3995 signs introduced in Unicode 16 (2024). This is also referred to as the **extended list**.
- Default glyphs for the 38 control characters introduced in Unicode 12 (2019) and Unicode 15 (2022).
- Various ligatures and auxiliary signs for the implementation of [HieroJax](https://github.com/nederhof/hierojax).

From the extended list only the **core** signs are included in the font. 
The 568 **non-core** signs are unverified and undocumented, and are thereby
pointless and were introduced in Unicode for all the wrong reasons (don't ask). 
In the font, the non-core signs have placeholder glyphs **nc**. A handful of non-core signs that were drawn by mistake are
kept in a separate font.

View the font in [GitHub Pages](https://nederhof.github.io/newgardiner/page0.html).

## Warning

There are countless unresolved issues in the extended list, such as inconsistencies between code charts and descriptions, and
inconsistencies between the new signs and the published encoding principles.
This font inevitably suffers from these issues as well and should therefore be considered as no more than a preliminary attempt 
to create a font covering the core signs.

Particularly egregious is that several signs from the basic list were misplaced to
new code points, while new shapes were assigned to old code points, without
any documented justification or open discussion.
Obviously this is unacceptable, as it invalidated overnight any encodings that were compiled in the past 16 years. 
The basic list needs to be restored to what it was in Unicode 5.2 as soon as possible.
A stable situation may however not exist until Unicode 18.

## Links

Latest Unicode code charts:

- [Basic list](https://unicode.org/charts/PDF/U13000.pdf)
- [Extended list](https://unicode.org/charts/PDF/U13460.pdf)
- [Format controls](https://unicode.org/charts/PDF/U13430.pdf)

Ancillary Unicode documentation:

- [Unikemet](https://www.unicode.org/Public/UCD/latest/ucd/Unikemet.txt)
- [Database](https://www.unicode.org/L2/L2023/23109-n5215-database.pdf)
- [Encoding principles](https://www.unicode.org/reports/tr57/tr57-4.html#EncodingPrinciples)

Unicode 5.2 (2009):

- [Basic list](https://www.unicode.org/charts/PDF/Unicode-5.2/U52-13000.pdf)
- [Document containing original Unikemet](https://www.unicode.org/L2/L2006/06354-n3181-egyptian.pdf)
- [Sources](https://www.unicode.org/L2/L2005/05313-Gardiner28-57.pdf)

Critiques of Unicode 16:

- [Side by side comparison Unicode 5.2 and Unicode 16](https://nederhof.github.io/newgardiner/unicode5to16compare0.html)
- [Corruption of the basic list in Unicode 16](https://nederhof.github.io/newgardiner/unicode5to16corruption.html)
- [Issues with the extended list in Unicode 16](https://nederhof.github.io/newgardiner/unicode16comments.html)
- [Legacy characters](https://nederhof.github.io/newgardiner/legacy.html)

<!--
Provisional Unicode 17 code charts:

- [Basic list (Beta Draft)](https://www.unicode.org/Public/draft/charts/blocks/U13000.pdf)
- [Extended list (Beta Draft)](https://www.unicode.org/Public/draft/charts/blocks/U13460.pdf)
-->

## Selected versions of the NewGardiner font

- 3.04 (2025-10-25)
	- Checked basic list against Unicode 5.2.
	- Some revisions of extended list.
- 3.03 (2025-06-17)
	- Global overhaul of extended list.
- 3.02 (2025-06-01)
	- Revised basic list to make all glyphs no wider or taller than 1 EM.
	- Minor revisions to extended list.
- 3.01 (2025-05-19)
	- Added the 3995 glyphs in the extended list (but with placeholders for non-core signs).
- 2.10 (2024-02-16)
	- Changed philological brackets.
- 2.07 (2023-05-24)
	- Added default glyphs for control characters and philological brackets.
- 2.05 (2020-11-09)
	- First release under OFL 1.1 license.
- 2.00 (2009-12-30)
	- Redesign of categories A, B, C.
- 1.00 (2009-01-07)
	- Initial release of the 1071 signs in the basic list.

