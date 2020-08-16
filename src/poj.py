from argparse import ArgumentParser, RawTextHelpFormatter
import fontforge


# Lookups and other features created by this script
LIGA_LOOKUP = "'liga' Standard Ligatures lookup POJ"
LIGA_SUBTABLE = "'liga' Standard Ligatures lookup POJ subtable"
CCMP_LOOKUP = "'ccmp' Glyph Composition POJ"
CCMP_SUBTABLE = "'ccmp' Glyph Composition POJ subtable"
MARK_LOOKUP = "'mark' Mark Positioning lookup POJ"
MARK_TOP_CNTR = "'mark' Mark Positioning lookup POJ top"
MARK_TOP_RIGHT = "'mark' Mark Positioning lookup POJ above right"
ANCH_TOP = "POJ_TOP_CENTER"
ANCH_TOP_RIGHT = "POJ_TOP_RIGHT"
DTLS_LOOKUP = 'Single Substitution dotless ij'
DTLS_SUBTABLE = 'Single Substitution dotless ij subtable'
CCMP_DTLS = "'ccmp' Contextual substitution dotless ij"
CCMP_SUBT = "'ccmp' Contextual substitution dotless ij subtable"
FEATURE_TAG = (("DFLT",("dflt")),("latn",("dflt")),)


def glyphEmpty(glyph):
    if glyph.foreground.isEmpty() and glyph.background.isEmpty and len(glyph.references) == 0:
        return True
    else:
        return False


def x_center(glyph):
    m = glyph
    return round((m.width + m.left_side_bearing - m.right_side_bearing)/2)


def hasDotlessi(font):
    glyph = font.createChar(0x0131)
    if (glyphEmpty(glyph)):
        return False
    if glyph.glyphname != 'dotlessi':
        glyph.glyphname = 'dotlessi'
    return True


def hasDotlessj(font):
    glyph = font.createChar(0x0237)
    if (glyphEmpty(glyph)):
        return False
    if glyph.glyphname != 'dotlessj':
        glyph.glyphname = 'dotlessj'
    return True


def checkAccents(font):
    error = False

    markDiacritics = [
        (0x0300, 'gravecomb'),
        (0x0301, 'acutecomb'),
        (0x0302, 'circumflexcomb'),
        (0x0304, 'macroncomb'),
        (0x0306, 'brevecomb'),
        (0x030b, 'hungarumlautcomb'),
        (0x030c, 'caroncomb'),
        (0x030d, 'vlinecomb'),
        (0x0358, 'dotcomb'),
    ]

    for uni, name in markDiacritics:
        glyph = font.createChar(uni)
        glyph.glyphname = name
        if glyphEmpty(glyph):
            error = True
            print('Missing glyph: ' + hex(uni) + ' ' + name)
        glyphCap = font.findEncodingSlot(name + '.cap')
        if glyphCap == -1:
            uniStrName = 'uni' + hex(uni)[2:].zfill(4).upper()
            glyphCap2 = font.findEncodingSlot(uniStrName + '.cap')

            if glyphCap2 == -1:
                error = True
                print('Missing glyph: ' + name + '.cap')
            else:
                font[glyphCap2].glyphname = name + '.cap'

    #Also check for dotless chars
    if not hasDotlessi(font):
        error = True
        print('Missing glyph: dotlessi uni0131')
    if not hasDotlessj(font):
        print('Missing (optional) glyph dotlessj uni0237, skipping...')

    if error:
        print('Please add missing glyphs. Exiting...')
        exit()


def fixONames(font):
    chars = [
        (0x00d2, 'Ograve'),
        (0x00d3, 'Oacute'),
        (0x00d4, 'Ocircumflex'),
        (0x00f2, 'ograve'),
        (0x00f3, 'oacute'),
        (0x00f4, 'ocircumflex'),
        (0x014c, 'Omacron'),
        (0x014d, 'omacron'),
        (0x014e, 'Obreve'),
        (0x014f, 'obreve'),
        (0x0150, 'Ohungarumlaut'),
        (0x0151, 'ohungarumlaut'),
        (0x01d1, 'Ocaron'),
        (0x01d2, 'ocaron')
    ]
    for uni, name in chars:
        glyph = font.createChar(uni)
        glyph.glyphname = name


def createLigaLookup(font):
    font.addLookup(
        LIGA_LOOKUP,
        'gsub_ligature',
        None,
        (("liga",FEATURE_TAG),)
    )
    font.addLookupSubtable(LIGA_LOOKUP, LIGA_SUBTABLE)

    font.addLookup(
        CCMP_LOOKUP,
        'gsub_ligature',
        None,
        (("ccmp",FEATURE_TAG),)
    )
    font.addLookupSubtable(CCMP_LOOKUP, CCMP_SUBTABLE)


def buildPOJligas(font, dxy):
    fixONames(font)
    createLigaLookup(font)

    pojLigatures = [
        ('A_vline', 'A', 'vlinecomb.cap', [('A', 'vlinecomb')]),
        ('a_vline', 'a', 'vlinecomb', [('a', 'vlinecomb')]),
        ('A_hungarumlaut', 'A', 'hungarumlautcomb.cap', [('A', 'hungarumlautcomb')]),
        ('a_hungarumlaut', 'a', 'hungarumlautcomb', [('a', 'hungarumlautcomb')]),
        ('E_vline', 'E', 'vlinecomb.cap', [('E', 'vlinecomb')]),
        ('e_vline', 'e', 'vlinecomb', [('e', 'vlinecomb')]),
        ('E_hungarumlaut', 'E', 'hungarumlautcomb.cap', [('E', 'hungarumlautcomb')]),
        ('e_hungarumlaut', 'e', 'hungarumlautcomb', [('e', 'hungarumlautcomb')]),
        ('I_vline', 'I', 'vlinecomb.cap', [('I', 'vlinecomb')]),
        ('i_vline', 'dotlessi', 'vlinecomb', [('i', 'vlinecomb')]),
        ('I_hungarumlaut', 'I', 'hungarumlautcomb.cap', [('I', 'hungarumlautcomb')]),
        ('i_hungarumlaut', 'dotlessi', 'hungarumlautcomb', [('i', 'hungarumlautcomb')]),
        ('M_grave', 'M', 'gravecomb.cap', [('M', 'gravecomb')]),
        ('m_grave', 'm', 'gravecomb', [('m', 'gravecomb')]),
        ('M_circumflex', 'M', 'circumflexcomb.cap', [('M', 'circumflexcomb')]),
        ('m_circumflex', 'm', 'circumflexcomb', [('m', 'circumflexcomb')]),
        ('M_caron', 'M', 'caroncomb.cap', [('M', 'caroncomb')]),
        ('m_caron', 'm', 'caroncomb', [('m', 'caroncomb')]),
        ('M_macron', 'M', 'macroncomb.cap', [('M', 'macroncomb')]),
        ('m_macron', 'm', 'macroncomb', [('m', 'macroncomb')]),
        ('M_vline', 'M', 'vlinecomb.cap', [('M', 'vlinecomb')]),
        ('m_vline', 'm', 'vlinecomb', [('m', 'vlinecomb')]),
        ('M_breve', 'M', 'brevecomb.cap', [('M', 'brevecomb')]),
        ('m_breve', 'm', 'brevecomb', [('m', 'brevecomb')]),
        ('M_hungarumlaut', 'M', 'hungarumlautcomb.cap', [('M', 'hungarumlautcomb')]),
        ('m_hungarumlaut', 'm', 'hungarumlautcomb', [('m', 'hungarumlautcomb')]),
        ('N_circumflex', 'N', 'circumflexcomb.cap', [('N', 'circumflexcomb')]),
        ('n_circumflex', 'n', 'circumflexcomb', [('n', 'circumflexcomb')]),
        ('N_macron', 'N', 'macroncomb.cap', [('N', 'macroncomb')]),
        ('n_macron', 'n', 'macroncomb', [('n', 'macroncomb')]),
        ('N_vline', 'N', 'vlinecomb.cap', [('N', 'vlinecomb')]),
        ('n_vline', 'n', 'vlinecomb', [('n', 'vlinecomb')]),
        ('N_breve', 'N', 'brevecomb.cap', [('N', 'brevecomb')]),
        ('n_breve', 'n', 'brevecomb', [('n', 'brevecomb')]),
        ('N_hungarumlaut', 'N', 'hungarumlautcomb.cap', [('N', 'hungarumlautcomb')]),
        ('n_hungarumlaut', 'n', 'hungarumlautcomb', [('n', 'hungarumlautcomb')]),
        ('O_vline', 'O', 'vlinecomb.cap', [('O', 'vlinecomb')]),
        ('o_vline', 'o', 'vlinecomb', [('o', 'vlinecomb')]),
        ('O_dot', 'O', 'dotcomb.cap', [('O', 'dotcomb')]),
        ('o_dot', 'o', 'dotcomb', [('o', 'dotcomb')]),
        ('O_acute_dot', 'Oacute', 'dotcomb.cap', [('Oacute', 'dotcomb'), ('O', 'acutecomb', 'dotcomb'), ('O', 'dotcomb', 'acutecomb')]),
        ('o_acute_dot', 'oacute', 'dotcomb', [('oacute', 'dotcomb'), ('o', 'acutecomb', 'dotcomb'), ('o', 'dotcomb', 'acutecomb')]),
        ('O_grave_dot', 'Ograve', 'dotcomb.cap', [('Ograve', 'dotcomb'), ('O', 'gravecomb', 'dotcomb'), ('O', 'dotcomb', 'gravecomb')]),
        ('o_grave_dot', 'ograve', 'dotcomb', [('ograve', 'dotcomb'), ('o', 'gravecomb', 'dotcomb'), ('o', 'dotcomb', 'gravecomb')]),
        ('O_circumflex_dot', 'Ocircumflex', 'dotcomb.cap', [('Ocircumflex', 'dotcomb'), ('O', 'circumflexcomb', 'dotcomb'), ('O', 'dotcomb', 'circumflexcomb')]),
        ('o_circumflex_dot', 'ocircumflex', 'dotcomb', [('ocircumflex', 'dotcomb'), ('o', 'circumflexcomb', 'dotcomb'), ('o', 'dotcomb', 'circumflexcomb')]),
        ('O_caron_dot', 'Ocaron', 'dotcomb.cap', [('Ocaron', 'dotcomb'), ('O', 'caroncomb', 'dotcomb'), ('O', 'dotcomb', 'caroncomb')]),
        ('o_caron_dot', 'ocaron', 'dotcomb', [('ocaron', 'dotcomb'), ('o', 'caroncomb', 'dotcomb'), ('o', 'dotcomb', 'caroncomb')]),
        ('O_macron_dot', 'Omacron', 'dotcomb.cap', [('Omacron', 'dotcomb'), ('O', 'macroncomb', 'dotcomb'), ('O', 'dotcomb', 'macroncomb')]),
        ('o_macron_dot', 'omacron', 'dotcomb', [('omacron', 'dotcomb'), ('o', 'macroncomb', 'dotcomb'), ('o', 'dotcomb', 'macroncomb')]),
        ('O_vline_dot', 'O_vline', 'dotcomb.cap', [('O', 'vlinecomb', 'dotcomb'), ('O', 'dotcomb', 'vlinecomb')]),
        ('o_vline_dot', 'o_vline', 'dotcomb', [('o', 'vlinecomb', 'dotcomb'), ('o', 'dotcomb', 'vlinecomb')]),
        ('O_breve_dot', 'Obreve', 'dotcomb.cap', [('Obreve', 'dotcomb'), ('O', 'brevecomb', 'dotcomb'), ('O', 'dotcomb', 'brevecomb')]),
        ('o_breve_dot', 'obreve', 'dotcomb', [('obreve', 'dotcomb'), ('o', 'brevecomb', 'dotcomb'), ('o', 'dotcomb', 'brevecomb')]),
        ('O_hungarumlaut_dot', 'Ohungarumlaut', 'dotcomb.cap', [('Ohungarumlaut', 'dotcomb'), ('O', 'hungarumlautcomb', 'dotcomb'), ('O', 'dotcomb', 'hungarumlautcomb')]),
        ('o_hungarumlaut_dot', 'ohungarumlaut', 'dotcomb', [('ohungarumlaut', 'dotcomb'), ('o', 'hungarumlautcomb', 'dotcomb'), ('o', 'dotcomb', 'hungarumlautcomb')]),
        ('U_vline', 'U', 'vlinecomb.cap', [('U', 'vlinecomb')]),
        ('u_vline', 'u', 'vlinecomb', [('u', 'vlinecomb')]),
    ]
    for name, base, mark, ligas in pojLigatures:
        ligaGlyph = font.createChar(-1, name)
        font.selection.select(base)
        font.copyReference()
        font.selection.select(ligaGlyph)
        font.paste()

        # Special positioning for the dots
        if 'dotcomb' in mark:
            if base[0] == 'O':
                x_pos = dxy[0] if dxy[0] is not None else font[font.findEncodingSlot('O')].width
                y_pos = dxy[1] if dxy[1] is not None else 0
            elif base[0] == 'o':
                x_pos = dxy[2] if dxy[2] is not None else font[font.findEncodingSlot('o')].width
                y_pos = dxy[3] if dxy[3] is not None else 0

        # Regular positioning for tone marks
        else:
            x_pos = x_center(ligaGlyph)
            y_pos = 0

        ligaGlyph.addReference(mark, [1, 0, 0, 1, x_pos, y_pos])

        # Add the ligatures to the lookup tables
        for liga in ligas:
            ligaGlyph.addPosSub(LIGA_SUBTABLE, liga)
            ligaGlyph.addPosSub(CCMP_SUBTABLE, liga)

def addMarkLookup(font):
    if MARK_LOOKUP not in font.gpos_lookups:
        font.addLookup(
            MARK_LOOKUP,
            "gpos_mark2base",
            None,
            (("mark",FEATURE_TAG),)
        )

def addPOJanchors(font, mark_y, uc_base_y, lc_base_y):
    # Add relevant lookup tables and subtables for mark2base
    addMarkLookup(font)
    font.addLookupSubtable(MARK_LOOKUP, MARK_TOP_CNTR)
    font.addAnchorClass(MARK_TOP_CNTR, ANCH_TOP)

    # Set mark anchors on tone diacritics
    marks = [
        'gravecomb',
        'acutecomb',
        'circumflexcomb',
        'macroncomb',
        'brevecomb',
        'hungarumlautcomb',
        'caroncomb',
        'vlinecomb'
    ]

    for name in marks:
        glyph = font[font.findEncodingSlot(name)]
        glyph.addAnchorPoint(
            ANCH_TOP, 'mark', x_center(glyph), mark_y)


    # Set base anchors on all alphabets
    # Capitals and with ascenders
    for name in list('ABCDEFGHIJKLMNOPQRSTUVWXYZbdfhijklt'):
        glyph = font[font.findEncodingSlot(name)]
        glyph.addAnchorPoint(
            ANCH_TOP, 'base', x_center(glyph), uc_base_y)

    # Lower case, no ascender
    for name in list('acegmnopqrsuvwxyz'):
        glyph = font[font.findEncodingSlot(name)]
        glyph.addAnchorPoint(
            ANCH_TOP, 'base', x_center(glyph), lc_base_y)

    # Dotlessi and j if available
    for name in ['dotlessi', 'dotlessj']:
        if name == 'dotlessj' and not hasDotlessj(font):
            continue
        glyph = font[font.findEncodingSlot(name)]
        glyph.addAnchorPoint(
            ANCH_TOP, 'base', x_center(glyph), lc_base_y)


def addDotAnchors(font, dxy, vxy):
    addMarkLookup(font)
    font.addLookupSubtable(MARK_LOOKUP, MARK_TOP_RIGHT)
    font.addAnchorClass(MARK_TOP_RIGHT, ANCH_TOP_RIGHT)

    # Set base anchor in the 'combining dot above right' uni0358
    glyph = font[font.findEncodingSlot('dotcomb')]
    dot_x = x_center(glyph) if dxy is None else dxy[0]
    dot_y = font.xHeight if dxy is None else dxy[1]
    glyph.addAnchorPoint(
        ANCH_TOP_RIGHT, 'mark', dot_x, dot_y)

    # Define all characters that can take the dot above right (all vowels)
    ucDottableChars = [
        ([
            (0x0041, 'A'),
            (0x00C0, 'Agrave'),
            (0x00C1, 'Aacute'),
            (0x00C2, 'Acircumflex'),
            (0x0100, 'Amacron'),
            (0x0102, 'Abreve'),
            (0x01CD, 'Acaron'),
        ], vxy[0], vxy[1]),
        ([
            (0x0045, 'E'),
            (0x00C8, 'Egrave'),
            (0x00C9, 'Eacute'),
            (0x00CA, 'Ecircumflex'),
            (0x0112, 'Emacron'),
            (0x0114, 'Ebreve'),
            (0x011A, 'Ecaron'),
        ], vxy[2], vxy[3]),
        ([
            (0x0049, 'I'),
            (0x00CC, 'Igrave'),
            (0x00CD, 'Iacute'),
            (0x00CE, 'Icircumflex'),
            (0x012A, 'Imacron'),
            (0x012C, 'Ibreve'),
            (0x01CF, 'Icaron'),
        ], vxy[4], vxy[5]),
        ([
            (0x004F, 'O'),
            (0x00D2, 'Ograve'),
            (0x00D3, 'Oacute'),
            (0x00D4, 'Ocircumflex'),
            (0x014C, 'Omacron'),
            (0x014E, 'Obreve'),
            (0x0150, 'Ohungarumlaut'),
            (0x01D1, 'Ocaron'),
        ], vxy[6], vxy[7]),
        ([
            (0x0055, 'U'),
            (0x00D9, 'Ugrave'),
            (0x00DA, 'Uacute'),
            (0x00DB, 'Ucircumflex'),
            (0x016A, 'Umacron'),
            (0x016C, 'Ubreve'),
            (0x0170, 'Uhungarumlaut'),
            (0x01D3, 'Ucaron'),
        ], vxy[8], vxy[9])]

    lcDottableChars = [([
            (0x0061, 'a'),
            (0x00E0, 'agrave'),
            (0x00E1, 'aacute'),
            (0x00E2, 'acircumflex'),
            (0x0101, 'amacron'),
            (0x0103, 'abreve'),
            (0x01CE, 'acaron'),
        ], vxy[10], vxy[11]), ([
            (0x0065, 'e'),
            (0x00E8, 'egrave'),
            (0x00E9, 'eacute'),
            (0x00EA, 'ecircumflex'),
            (0x0113, 'emacron'),
            (0x0115, 'ebreve'),
            (0x011B, 'ecaron'),
        ], vxy[12], vxy[13]), ([
            (0x0069, 'i'),
            (0x00EC, 'igrave'),
            (0x00ED, 'iacute'),
            (0x00EE, 'icircumflex'),
            (0x012B, 'imacron'),
            (0x012D, 'ibreve'),
            (0x01D0, 'icaron'),
        ], vxy[14], vxy[15]), ([
            (0x006F, 'o'),
            (0x00F2, 'ograve'),
            (0x00F3, 'oacute'),
            (0x00F4, 'ocircumflex'),
            (0x014D, 'omacron'),
            (0x014F, 'obreve'),
            (0x0151, 'ohungarumlaut'),
            (0x01D2, 'ocaron'),
        ], vxy[16], vxy[17]), ([
            (0x0075, 'u'),
            (0x00F9, 'ugrave'),
            (0x00FA, 'uacute'),
            (0x00FB, 'ucircumflex'),
            (0x016B, 'umacron'),
            (0x016D, 'ubreve'),
            (0x0171, 'uhungarumlaut'),
            (0x01D4, 'ucaron'),
        ], vxy[18], vxy[19])]

    for bases, xpos, ypos in ucDottableChars:
        for uni, name in bases:
            glyph = font[font.findEncodingSlot(uni)]
            glyph.glyphname = name
            xpos = glyph.width if xpos is None else xpos
            ypos = font.capHeight if ypos is None else ypos
            glyph.addAnchorPoint(ANCH_TOP_RIGHT, 'base', xpos, ypos)

    for bases, xpos, ypos in lcDottableChars:
        for uni, name in bases:
            glyph = font[font.findEncodingSlot(uni)]
            glyph.glyphname = name
            xpos = glyph.width if xpos is None else xpos
            ypos = font.xHeight if ypos is None else ypos
            glyph.addAnchorPoint(ANCH_TOP_RIGHT, 'base', xpos, ypos)


def subDotlessIJ(font):
    font.addLookup(
        DTLS_LOOKUP,
        'gsub_single',
        None,
        (("dtls",FEATURE_TAG),)
    )
    font.addLookupSubtable(
        DTLS_LOOKUP,
        DTLS_SUBTABLE
    )
    font[font.findEncodingSlot('i')].addPosSub(DTLS_SUBTABLE, 'dotlessi')
    if hasDotlessj(font):
        font[font.findEncodingSlot('j')].addPosSub(DTLS_SUBTABLE, 'dotlessj')

    font.addLookup(
        CCMP_DTLS,
        'gsub_contextchain',
        None,
        (("ccmp",FEATURE_TAG),)
    )
    accentList = 'acutecomb gravecomb circumflexcomb macroncomb brevecomb hungarumlautcomb caroncomb vlinecomb'
    dotlesschars = '[i j]' if hasDotlessj(font) else '[i]'
    font.addContextualSubtable(
        CCMP_DTLS,
        CCMP_SUBT,
        'coverage',
        dotlesschars + ' @<' + DTLS_LOOKUP + '> | [' + accentList + ']'
    )

if __name__ == '__main__':
    desc = ('********************\n'
            '*** build_poj.py ***\n'
            '********************\n\n'
            'Add POJ support to a FontForge .sfd (SplineFontDatabase) font file.\n\n'
            ' - OpenType features included: ccmp, liga, and mark.\n'
            ' - Glyphs: all tone diacritics on aeimnou and o-dot\n'
            ' - Mark2Base:\n'
            '    - tone anchors for all letters A-Za-z\n'
            '    - dot above right anchors for vowels\n\n'
            'It is recommended that you first run the script without'
            ' any positioning data and then adjust as needed.\n\n'
            'For best results, ensure that your font has all needed diacritics:\n\n'
            ' - U+0300,0301,0302,0304,0306,030B,030C,030D,0358\n'
            ' - uppercase versions of above, named with `.cap` suffix\n'
            ' - all diacritics should be centered in a zero-width glyph\n'
            ' - dotlessi (U+0131) is required, dotlessj (U+0237) is optional\n\n'
            'ATTENTION! Before running this script, use the script\n'
            '    `FillUnicodeDiacritics.pe`\n'
            'to build any missing single codepoint diacritics, this step is required!\n\n'
            'Example: ffpython build_poj.py --input MyFont.sfd \\\n'
            '                               --output output.sfd \\\n'
            '                               --oxy 670 -40 535 0 \\   # Ox Oy ox oy\n'
            '                               --vxy 500 527 587 658 339 707 647 667 713 720 \\   # uppercase AEIOU\n'
            '                                     431 417 450 432 272 366 496 448 473 505     # lowercase aeiou')
    parser = ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', '--input', type=str, required=True, help='The input .sfd font file')
    parser.add_argument('-o', '--output', type=str, default='output.sfd', help='The output .sfd font file (default: output.sfd)')
    parser.add_argument('--oxy', type=int, nargs=4, help='XY-translation for dots next to Oo [Ox Oy ox oy] (default: 0 0 0 0)')
    parser.add_argument('--ty', type=int, help='Y-coordinate for tone mark anchors (default: x-height)')
    parser.add_argument('--uy', type=int, help='Y-coordinate for uppercase & ascender anchors (default: cap-height)')
    parser.add_argument('--ly', type=int, help='Y-coordinate for lowercase anchors (default: x-height)')
    parser.add_argument('--dxy', type=int, nargs=2, help='XY-coords for dot (uni0358) anchor (default: 0 x-height)')
    parser.add_argument('--vxy', type=int, nargs=20, help='XY-coords for dots next to vowels AEIOUaeiou [Ax Ay...ux uy]')
    parser.add_argument('--skip-dotless', action='store_true', help='Do not replace ij with dotlessij')
    parser.add_argument('--skip-poj-anchors', action='store_true', help='Do not add top center anchors')

    args = parser.parse_args()

    f1 = fontforge.open(args.input)

    # Prepare metrics
    mark_y = f1.xHeight if args.ty is None else args.ty
    uc_base_y = f1.capHeight if args.uy is None else args.uy
    lc_base_y = f1.xHeight if args.ly is None else args.ly
    o_dot_translate_xy = [None] * 4 if args.oxy is None else args.oxy
    dot_mark_anchor_xy = args.dxy
    vowel_top_right_xy = [None] * 20 if args.vxy is None else args.vxy

    # Test font for missing glyphs
    checkAccents(f1)

    # Build POJ compatibility
    buildPOJligas(f1, o_dot_translate_xy)
    if args.skip_poj_anchors is False:
        addPOJanchors(f1, mark_y, uc_base_y, lc_base_y)
    if args.skip_dotless is False:
        subDotlessIJ(f1)
    addDotAnchors(f1, dot_mark_anchor_xy, vowel_top_right_xy)

    # Output new font
    f1.save('output.sfd' if args.output is None else args.output)
