# POJ Fonts

See individual font folders for license information.

PRs welcome!

![Font preview](https://github.com/aiongg/POJFonts/blob/master/preview.png?raw=true)

## Creating a font

See the following video tutorial for complete instructions:

[![Súi Pe̍h-ōe-jī, tāu-hū chài-hōe! POJ FontForge Tutorial - Add POJ support to any open source font
](https://img.youtube.com/vi/_KAJxOPsk7w/0.jpg)](https://www.youtube.com/watch?v=_KAJxOPsk7w)

## Required data

Refer to the file [`charset.txt`](charset.txt) for all of the data necessary to make a POJ-compatible font. Any submitted fonts should include all of the glyphs, unicode codepoints, and OpenType positioning and ligature tables required for compatibility. Private Use Area codepoints E400-E435 are optional, but highly recommended to ensure your font will be supported in legacy applications that do not support OpenType.

I. SINGLE CODE POINTS - LATIN LETTERS
II. SINGLE CODEPOINTS - COMBINING CHARACTERS
III. MARK-TO-BASE LOOKUPS
IV. LIGATURES AND PRIVATE USE AREA (NON-STANDARD)
V. 3-CODEPOINT LIGATURE LOOKUP TABLES

The corresponding Excel sheet `charset.xlsx` displays all characters and
Unicode points for easy reference when creating or modifying a font.

In order to maintain consistency among fonts included in this repository,
please make a copy of all ligature glyphs (glyphs which comprise two
or more Unicode code points), and add Private Use Area codepoints
(as listed in `charset.txt` Sec. IV) for use in legacy software that
does not support the necessary OpenType features.
