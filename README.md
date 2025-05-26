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
The **non-core** signs are unverified and undocumented, and are thereby
useless for any practical purposes and were introduced in Unicode for all the wrong reasons (don't ask). 
In the font, the non-core signs have placeholder glyphs **nc**. A handful of non-core signs that were drawn by mistake are
kept in a separate font.

View the font in [GitHub Pages](https://nederhof.github.io/newgardiner/).

## Warning

There are countless unresolved issues in the extended list, such as inconsistencies between code charts and descriptions, and
inconsistencies between the new signs and the published encoding principles.
This font inevitably suffers from these issues as well and should therefore be considered as no more than a preliminary attempt 
to create a font covering the core signs.

Particularly egregious is that some signs from the basic list were misplaced to
new code points, while new shapes were assigned to old code points.
Obviously this is unacceptable and the basic list needs to be restored to what it was in Unicode 5.2 as soon as possible.
A stable situation may not exist until Unicode 18.

## Links

Latest Unicode code charts:

- [Basic list](https://unicode.org/charts/PDF/U13000.pdf)
- [Extended list](https://unicode.org/charts/PDF/U13460.pdf)
- [Format controls](https://unicode.org/charts/PDF/U13430.pdf)

Unicode 5.2 (2009) code charts:

- [Basic list](https://www.unicode.org/charts/PDF/Unicode-5.2/U52-13000.pdf)

Ancillary Unicode documentation:

- [Unikemet](https://www.unicode.org/Public/UCD/latest/ucd/Unikemet.txt)
- [Database](https://www.unicode.org/L2/L2023/23109-n5215-database.pdf)
- [Encoding principles](https://www.unicode.org/reports/tr57/tr57-4.html)

Corruption of the basic list:

- [Side by side comparison Unicode 5.2 and Unicode 16](https://nederhof.github.io/unicode5to16compare.html)
- [List of differences Unicode 5.2 versus Unicode 16](https://nederhof.github.io/unicode5to16corruption.html)

## Selected versions of the NewGardiner font

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

