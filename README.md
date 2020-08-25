# POJ Fonts

See individual font folders for license information.

PRs welcome!

![Font preview](https://github.com/aiongg/POJFonts/blob/master/preview.png?raw=true)

## An-chong Soat-bêng

Táng-ló͘ jī-thé: [POJFonts.zip](https://github.com/aiongg/POJFonts/releases/download/v1/POJFonts-v1.zip)

Kā lí siūⁿ-beh an-chong ê jī-thé chhi̍h--loeh an-chong, koh-lâi tī lí teh sú-iōng ê nńg-thé lâi kéng jī-thé to̍h ē-sái.

## Creating a font

### Automated via `poj.py`

#### Setup fontforge and python

Make sure Python >3 and the `fontforge` module are installed. On Windows, you can open a fontforge ready terminal using the `fontforge-console.bat` file found in your FontForge installation directory (e.g., `C:\Program Files (x86)\FontForgeBuilds\fontforge-console.bat`). You may also install via `pip install python-fontforge`.

Run the `poj.py -h` command for help instructions:

```
python /path/to/poj.py -h
```

or

```
ffpython /path/to/poj.py -h
```

#### Prepare the glyphs

**2x Letter Glyphs**

The following 2 letter glyphs are required:

```
uni0131 LATIN SMALL LETTER DOTLESS I (dotlessi, ı)
uni207F SUPERSCRIPT LATIN SMALL LETTER N (ⁿ)
```

- `dotlessi` can be created by copying the `i` to the slot `uni0131` and deleting the dot
- `ⁿ` can be created by copying `n` and using `Element > styles > Change Glyph` to resize as necessary, typically around 50-60% of the original size.

**11x Diacritic Glyphs**

The following 11 diacritic glyphs are required:

```
name     diacritic
uni0300  COMBINING GRAVE ACCENT         tone 3
uni0301  COMBINING ACUTE ACCENT         tone 2
uni0302  COMBINING CIRCUMFLEX ACCENT    tone 5
uni0304  COMBINING MACRON               tone 7
uni0306  COMBINING BREVE                tone 9
uni030A  COMBINING RING ABOVE           Pha̍k-fa-sṳ
uni030B  COMBINING DOUBLE ACUTE ACCENT  tone 9 (MOE)
uni030C  COMBINING CARON                tone 6 (Hái-kháu-khiuⁿ)
uni030D  COMBINING VERTICAL LINE ABOVE  tone 8
uni0324  COMBINING DIAERESIS BELOW      Pha̍k-fa-sṳ, Hái-kháu-khiuⁿ
uni0358  COMBINING DOT ABOVE RIGHT      long o, sometimes e i u
```

**Uppercase and lowercase diacritics**

Separate upper case letter accents are *optional* but recommended. If you do not create them separately, the normal lower case accents will be re-used. To design separate upper case accents, add a new glyph slot with a Unicode value of -1, use the same name and append the suffix `.cap` to the name, e.g., `uni0300.cap, uni0301.cap, ...`. The upper case versions of the accents are typically shorter than the lowercase versions, to prevent the accented uppercase letters from being too tall. For small caps, append `.sc`.

**Dotted E I and U**

Note that some versions of Pehoeji use dotted E, I, and U in addition to dotted O to represent various regional accents. These are included as `mark2base` lookups by default, and can be disabled with the `--skip-dot-anchors` option. If you want to include them (*recommended*), it is best to run the script once and then use the Lookup `mark2base` window for positioning the anchors on the base glyphs; `A` is included for completeness. To do this, navigate to:

```
Element Menu
> Font Info
> Lookups
> GPOS
> 'mark' Mark Positioning lookup POJ
> 'mark' Mark Positioning lookup POJ above right
> Edit Data
> POJ_TOP_RIGHT
> Anchor Control
```

Then, select any base glyph starting with an upper case `A`, and position the anchor as desired. Note the X and Y coordinates. Repeat for glyphs `E I O U a e i o u`, and then pass all coordinates to the `--vowel-dots` option of the script. For example:

```
           # Ax  Ay  Ex  Ey  Ix  Iy  Ox  Oy  Ux  Uy  ax  ay  ex  ey  ix  iy  ox  oy  ux  uy
--vowel-dots 500 527 587 658 339 707 647 667 713 720 431 417 450 432 272 366 496 448 473 505
```

**Auto-Kerning**

Check some common letter pairs that may require kerning, such as `Tn`. If kerning is required to move the letters closer together. use the `--auto-kern` option to guess kerning, or `--kern-sep` to specify it manually. `--kern-sep` takes 2 numbers as arguments:

1. The desired separation in EMs (e.g., 100)
2. The closeness of the glyph classes (1 = exact match, 20 = loose match; try different values to see the results)

The `--auto-kern` option uses default values equivalent to `--kern-sep 200 20`.

#### Cleaning up

After running the script, check the accented characters in the range `uni00C0 - uni01F9` and unencoded glyphs at the end of the file. Position any accents as necessary, including the dots next to `O` and `o`. Set the advance width for dotted `O` and `o`, using the Metrics Window (e.g., `/o_dotaboveright/h`) to determine an appropriate value. You can set the width for multiple glyphs at once by selecting them in the font view window.

#### Naming

Name your font according to restrictions provided in the license. For OFL fonts, you may not re-use the original name. Be sure to set both the `PS Names` and `TTF Names` in the `Font Information` dialog. Add any additional copyright and license information as required.

#### Export

For best results, export your font as `OpenType (CFF)` type. In the `Options` dialog, select: `Hints, Flex Hints, PS Glyph Names, OpenType` and deselect everything else.

#### Additional information

c.f. [FontForge Python reference](https://fontforge.org/docs/scripting/python.html)

### Tips for creating the fonts manually in FontForge

See the following video tutorial for manual instructions:

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
