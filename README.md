# NewGardiner font of Egyptian Hieroglyphs

This TrueType font was created at the [University of St Andrews](https://www.st-andrews.ac.uk/) using [FontForge](https://fontforge.org/en-US/). It is released under the SIL OFL 1.1 license.

It includes:

- All 1071 hieroglyphic signs introduced in Unicode 5.2 (2009). This is also referred to as the **basic list**.
- One additional sign introduced in Unicode 12 (2019).
- Most of the 3995 signs introduced in Unicode 16 (2024). This is also referred to as the **extended list**.
- Default glyphs for the 38 control characters introduced in Unicode 12 (2019) and Unicode 15 (2022).
- Various ligatures and auxiliary signs for the implementation of [HieroJax](https://github.com/nederhof/hierojax)
and [hieropy](https://github.com/nederhof/hieropy).

From the extended list only the **core** signs are included in the font. The 568 **non-core** signs are unverified and undocumented, and were introduced in Unicode for all the wrong reasons (don't ask). A handful of non-core signs that were drawn by mistake are kept in a separate font.

**Do not ask me to add non-core signs. I cannot draw something if I don't know what that something is.**

View the font in [GitHub Pages](https://nederhof.github.io/newgardiner/page0.html).

## Warning

There are countless unresolved issues in the extended list, such as inconsistencies between code charts and descriptions, and inconsistencies between the new signs and the published encoding principles. This font inevitably suffers from these issues as well and should therefore be considered as no more than a preliminary attempt to create a font covering the core signs. Some of these issues may be corrected in Unicode 18, but many will probably not be.

## Links

Latest Unicode code charts:

- [Basic list](https://unicode.org/charts/PDF/U13000.pdf)
- [Extended list](https://unicode.org/charts/PDF/U13460.pdf)
- [Format controls](https://unicode.org/charts/PDF/U13430.pdf)

Ancillary Unicode documentation:

- [Unikemet](https://www.unicode.org/Public/UCD/latest/ucd/Unikemet.txt)
- [Database](https://www.unicode.org/wg2/docs/n5240-hieroglyphs-DB.pdf)
- [Encoding principles](https://www.unicode.org/reports/tr57/tr57-4.html#EncodingPrinciples)

Unicode 5.2 (2009):

- [Basic list](https://www.unicode.org/charts/PDF/Unicode-5.2/U52-13000.pdf)
- [Document containing original Unikemet](https://www.unicode.org/L2/L2007/07097-n3237-egyptian.pdf)
- [Sources (Gardiner's lists)](https://www.unicode.org/L2/L2005/05313-Gardiner28-57.pdf)
- [Sources (Gardiner's lists plus additional material)](https://www.unicode.org/L2/L2006/06355-n3182-egyptian-sources.pdf)

Critiques of Unicode 16:

- [Side by side comparison Unicode 5.2 and Unicode 16](https://nederhof.github.io/newgardiner/unicode5to16compare0.html)
- [Corruption of the basic list in Unicode 16](https://nederhof.github.io/newgardiner/unicode5to16corruption.html)
- [Issues with the extended list in Unicode 16](https://nederhof.github.io/newgardiner/unicode16comments.html)
- [Legacy characters](https://nederhof.github.io/newgardiner/legacy.html)
- [Reply regarding corruption of the basic list](https://www.unicode.org/L2/L2026/26060-answer-to-26059.pdf)

Drafts of Unicode 18:

- [Basic list](https://www.unicode.org/charts/PDF/Unicode-18.0/U180-13000.pdf)
- [Extended list](https://www.unicode.org/charts/PDF/Unicode-18.0/U180-13460.pdf)
- [Unikemet](https://www.unicode.org/Public/draft/ucd/Unikemet.txt)

<!--
Provisional Unicode 17 code charts:

- [Basic list (Beta Draft)](https://www.unicode.org/Public/draft/charts/blocks/U13000.pdf)
- [Extended list (Beta Draft)](https://www.unicode.org/Public/draft/charts/blocks/U13460.pdf)
-->

## Selected versions of the NewGardiner font

- 3.08 (2026-03-31)
	- Simplified several glyphs in basic list.
- 3.07 (2026-02-14)
	- Several corrections.
- 3.06 (2025-12-21)
	- Placeholder glyphs for non-core signs removed.
- 3.05 (2025-12-13)
	- Added one ligature.
	- A few minor revisions.
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
