from argparse import ArgumentParser, RawTextHelpFormatter
import math
import re
import unicodedata as ud
import fontforge

def log(msg):
    print(msg)

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
CCMP_DTLS_SUBT = "'ccmp' Contextual substitution dotless ij subtable"
SMCP_LOOKUP = "'smcp' Lowercase to small capitals POJ"
SMCP_SUBT = "'smcp' Lowercase to small capitals POJ subtable"
C2SC_LOOKUP = "'c2sc' Capitals to small capitals POJ"
C2SC_SUBT = "'c2sc' Capitals to small capitals POJ subtable"
FEATURE_TAG = (("DFLT",("dflt")),("latn",("dflt")),)

ABC_UC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ABC_LC = 'abcdefghijklmnopqrstuvwxyz'

M_GRAV = 'grave'
M_ACUT = 'acute'
M_CIRC = 'circumflex'
M_MACR = 'macron'
M_BREV = 'breve'
M_RING = 'ring'
M_HNGU = 'hungarumlaut'
M_CARN = 'caron'
M_VLIN = 'vline'
M_DIAB = 'diaresisbelow'
M_DOTA = 'dotaboveright'

DTLS_I = (0x0131, 'dotlessi')
DTLS_J = (0x0237, 'dotlessj')

ACCENTED_CHARS = [
    (0x00C0, f'A{M_GRAV}'), (0x00C1, f'A{M_ACUT}'), (0x00C2, f'A{M_CIRC}'), (0x00C5, f'A{M_RING}'),
    (0x00C8, f'E{M_GRAV}'), (0x00C9, f'E{M_ACUT}'), (0x00CA, f'E{M_CIRC}'),
    (0x00CC, f'I{M_GRAV}'), (0x00CD, f'I{M_ACUT}'), (0x00CE, f'I{M_CIRC}'),
    (0x00D2, f'O{M_GRAV}'), (0x00D3, f'O{M_ACUT}'), (0x00D4, f'O{M_CIRC}'),
    (0x00D9, f'U{M_GRAV}'), (0x00DA, f'U{M_ACUT}'), (0x00DB, f'U{M_CIRC}'),
    (0x00E0, f'a{M_GRAV}'), (0x00E1, f'a{M_ACUT}'), (0x00E2, f'a{M_CIRC}'), (0x00E5, f'a{M_RING}'),
    (0x00E8, f'e{M_GRAV}'), (0x00E9, f'e{M_ACUT}'), (0x00EA, f'e{M_CIRC}'),
    (0x00EC, f'i{M_GRAV}'), (0x00ED, f'i{M_ACUT}'), (0x00EE, f'i{M_CIRC}'),
    (0x00F2, f'o{M_GRAV}'), (0x00F3, f'o{M_ACUT}'), (0x00F4, f'o{M_CIRC}'),
    (0x00F9, f'u{M_GRAV}'), (0x00FA, f'u{M_ACUT}'), (0x00FB, f'u{M_CIRC}'),
    (0x0100, f'A{M_MACR}'), (0x0101, f'a{M_MACR}'), (0x0102, f'A{M_BREV}'), (0x0103, f'a{M_BREV}'),
    (0x0112, f'E{M_MACR}'), (0x0113, f'e{M_MACR}'), (0x0114, f'E{M_BREV}'), (0x0115, f'e{M_BREV}'),
    (0x011A, f'E{M_CARN}'), (0x011B, f'e{M_CARN}'),
    (0x012A, f'I{M_MACR}'), (0x012B, f'i{M_MACR}'), (0x012C, f'I{M_BREV}'), (0x012D, f'i{M_BREV}'),
    (0x0143, f'N{M_ACUT}'), (0x0144, f'n{M_ACUT}'), (0x0147, f'N{M_CARN}'), (0x0148, f'n{M_CARN}'),
    (0x014C, f'O{M_MACR}'), (0x014D, f'o{M_MACR}'), (0x014E, f'O{M_BREV}'), (0x014F, f'o{M_BREV}'),
    (0x0150, f'O{M_HNGU}'), (0x0151, f'o{M_HNGU}'),
    (0x016A, f'U{M_MACR}'), (0x016B, f'u{M_MACR}'), (0x016C, f'U{M_BREV}'), (0x016D, f'u{M_BREV}'),
    (0x016E, f'U{M_RING}'), (0x016F, f'u{M_RING}'), (0x0170, f'U{M_HNGU}'), (0x0171, f'u{M_HNGU}'),
    (0x01CD, f'A{M_CARN}'), (0x01CE, f'a{M_CARN}'),
    (0x01CF, f'I{M_CARN}'), (0x01D0, f'i{M_CARN}'),
    (0x01D1, f'O{M_CARN}'), (0x01D2, f'o{M_CARN}'),
    (0x01D3, f'U{M_CARN}'), (0x01D4, f'u{M_CARN}'),
    (0x01F8, f'N{M_GRAV}'), (0x01F9, f'n{M_GRAV}'),
    (0x1E3E, f'M{M_ACUT}'), (0x1E3F, f'm{M_ACUT}'),
    (0x1E72, f'U{M_DIAB}'), (0x1E73, f'u{M_DIAB}')
]

UNI_DIACRITICS = [(0x0300, M_GRAV), (0x0301, M_ACUT), (0x0302, M_CIRC),
                  (0x0304, M_MACR), (0x0306, M_BREV), (0x030A, M_RING),
                  (0x030B, M_HNGU), (0x030C, M_CARN), (0x030D, M_VLIN),
                  (0x0324, M_DIAB), (0x0358, M_DOTA)]
TONE_MARKS = [M_ACUT, M_GRAV, M_CIRC, M_CARN, M_MACR, M_VLIN, M_BREV, M_HNGU, M_RING]
TONE_MARKS_COMB = list(map(lambda x: x + 'comb', TONE_MARKS))


def getAccentedCharName(base, mark):
    if mark is None or len(mark) == 0:
        return base

    uni = next(x[0] for x in UNI_DIACRITICS if x[1] == mark)
    char = ud.normalize('NFC', base + chr(uni))
    if len(char) == 1:
        return base + mark
    else:
        return base + '_' + mark


def getOULigaSet(char):
    """char: one of O, U, o, or u
    Build the ligature sets for:
        O + <accent> + dotaboveright
        U + <accent> + diaresisbelow
    """
    if char in 'Oo':
        mod = M_DOTA
    elif char in 'Uu':
        mod = M_DIAB
    else:
        log('Only O and U get modifier ligatures')
        exit()

    ligaSet = []
    modComb = mod + 'comb'
    modCase = f'{modComb}.cap' if char.isupper() else modComb
    if (char.lower() == 'o'):
        ligaSet.append((f'{char}_{mod}', char, modCase, [(char, modComb)]))
    for tone in TONE_MARKS:
        base = getAccentedCharName(char, tone)
        name = f'{base}_{mod}'
        tone = tone + 'comb'
        ligas = [(base, modComb), (char, tone, modComb), (char, modComb, tone)]
        if char.lower() == 'u':
            ligas.append((f'{char}{mod}'))
        ligaSet.append((name, base, modCase, ligas))
    return ligaSet


def getLigaSet():
    """Build the ligature glyph data table, which is a list containing tuples:
        (name, base, mark, lookups)
    Where `lookups` is the list of entries to append to the ligature lookup
    for accessing this glyph

    This method assumes that all characters with diacritics that do not have
    a pre-defined unicode codepoint (e.g., latin + "vertical line above")
    must be added to the font
    """
    ligaSet = []
    for base in 'AEIMNOUaeimnou':
        for mark in TONE_MARKS:
            name = getAccentedCharName(base, mark)
            if '_' in name:
                mark += 'comb'
                markCase = f'{mark}.cap' if base[0].isupper() else mark
                liga = (name, base, markCase, [(base, mark)])
                ligaSet.append(liga)
        if base in 'OUou':
            ligaSet += getOULigaSet(base)

    return ligaSet

LIGA_SET = getLigaSet()

def rm_modifiers(i):
    return lambda x: (M_DOTA not in x[i]) and (M_DIAB not in x[i])
DOT_ANCHOR_SET = list('AEIOUaeiou') \
               + [x[1] for x in filter(rm_modifiers(1), ACCENTED_CHARS) if re.match('^[AEIOUaeiou]', x[1])] \
               + [x[0] for x in filter(rm_modifiers(0), LIGA_SET) if re.match('^[AEIOUaeiou]', x[0])]


def uni_name_from_int(codepoint):
    """Takes an int codepoint and returns a string of the standard
    glyph name format:
        uniXXXX
    Where XXXX is the 4-character hexadecimal value
    """
    return 'uni' + hex(codepoint)[2:].zfill(4).upper()


class POJFont:
    def __init__(self, fontfile):
        self.font = fontforge.open(fontfile)
        self.glyphList = []


    def run(self, args):
        self.scSuffix = args.sc_suffix
        self.vowelDotXY = args.vowel_dots

        # mark_y = self.font.xHeight if args.ty is None else args.ty
        # uc_base_y = self.font.capHeight if args.uy is None else args.uy
        # lc_base_y = self.font.xHeight if args.ly is None else args.ly
        # o_dot_translate_xy = [None] * 4 if args.oxy is None else args.oxy

        # Test font for missing glyphs
        self.checkAlphas()
        self.checkDiacritics(checkSmcp=args.sc_suffix is not None)
        self.checkDotlessi()
        self.checkOrBuildAccentedUnicode()

        # Build POJ compatibility
        if args.skip_ligas is False:
            self.buildPOJligas()
        if args.skip_poj_anchors is False:
            self.addPOJanchors()
        if args.skip_dotlessi is False:
            self.addSubDotlessIJLookups()
        if args.skip_dot_anchors is False:
            self.addDotAnchors()
        if args.sc_suffix is not None:
            self.buildSmallCaps()

        if args.auto_kern is True:
            self.autoKern()
        elif args.kern_sep is not None:
            self.autoKern(args.kern_sep[0], args.kern_sep[1])

        # Output new font
        self.font.save('output.sfd' if args.output is None else args.output)


    """
    Utility methods
    """
    def getGlyph(self, nameOrUni):
        if isinstance(nameOrUni, fontforge.glyph):
            return nameOrUni
        slot = self.font.findEncodingSlot(nameOrUni)
        if slot == -1:
            return None

        try:
            glyph = self.font[slot]
            return glyph
        except TypeError:
            return None


    def addLookup(self, lname, ltype, feature, after_lname=None):
        if ltype.startswith('gpos'):
            prop = 'gpos_lookups'
        elif ltype.startswith('gsub'):
            prop = 'gsub_lookups'

        if lname not in getattr(self.font, prop):
            if after_lname is None:
                self.font.addLookup(lname, ltype, None, ((feature, FEATURE_TAG),) )
            else:
                self.font.addLookup(lname, ltype, None, ((feature, FEATURE_TAG),), after_lname)


    def addLookupSubtable(self, lookup, subtable):
        subtables = self.font.getLookupSubtables(lookup)
        if subtable not in subtables:
            self.font.addLookupSubtable(lookup, subtable)


    def copyRefTo(self, orig, dest):
        self.font.selection.select(orig)
        self.font.copyReference()
        self.font.selection.select(dest)
        self.font.paste()


    def italicOffsetX(self, y1, y2):
        """Do triangle math things."""
        if not isinstance(self.font.italicangle, (int, float)) or y1 == y2:
            return 0
        ia_deg = math.fabs(self.font.italicangle)

        alpha = math.radians(ia_deg)
        beta = math.radians(90 - ia_deg)
        b = y2 - y1
        a = b * math.sin(alpha) / math.sin(beta)
        return round(a)


    def italicOffsetFromGlyphMid(self, baseGlyph, height):
        bounds = baseGlyph.boundingBox()
        y_mid = (bounds[1] + bounds[3]) / 2
        return self.italicOffsetX(y_mid, height)


    def italicOffsetBetweenGlyphs(self, lower, upper):
        lbounds = lower.boundingBox()
        ubounds = upper.boundingBox()
        y1 = (lbounds[1] + lbounds[3]) / 2
        y2 = (ubounds[1] + ubounds[3]) / 2
        return self.italicOffsetX(y1, y2)


    def centerX(self, nameOrGlyph):
        if isinstance(nameOrGlyph, str):
            glyph = self.getGlyph(nameOrGlyph)
        else:
            glyph = nameOrGlyph
        bounds = glyph.boundingBox()
        return round((bounds[2] + bounds[0]) / 2)


    """
    Glyph completeness checks
    """
    def registerGlyph(self, name):
        if name not in self.glyphList \
                and name not in TONE_MARKS_COMB \
                and name not in [M_DOTA + 'comb', M_DIAB + 'comb']:
            self.glyphList.append(name)


    def checkExistsAndSetName(self, codepoint, name):
        slot = self.font.findEncodingSlot(codepoint)
        if slot == -1:
            return False
        try:
            glyph = self.font[slot]
        except TypeError:
            return False

        if glyph.glyphname != name:
            glyph.glyphname = name

        self.registerGlyph(name)
        return glyph


    def hasDotlessi(self):
        return self.checkExistsAndSetName(DTLS_I[0], DTLS_I[1])


    def hasDotlessj(self):
        return self.checkExistsAndSetName(DTLS_J[0], DTLS_J[1])


    def checkDotlessi(self):
        error = False
        if not self.hasDotlessi():
            error = True
            log('Missing glyph: dotlessi uni0131')
        if not self.hasDotlessj():
            log('Missing (optional) glyph dotlessj uni0237, skipping...')


    def checkOrCreateAltAccent(self, uni, name, suf):
        altName = name + '.' + suf
        uniName = uni_name_from_int(uni) + '.' + suf

        glyph = self.getGlyph(altName)
        if glyph is None:
            glyph = self.getGlyph(uniName)

        if glyph is not None:
            glyph.glyphname = altName
            return glyph

        log('Building alternate accent glyph: ' + altName)
        glyph = self.font.createChar(-1, altName)
        glyph.addReference(name)
        return glyph


    def checkNsup(self):
        glyph = self.getGlyph(0x207f)
        if glyph is None:
            glyph = self.getGlyph('uni207F')
        if glyph is None:
            log('Missing superscript n (uni207F)')
            return False
        glyph.glyphname = 'uni207F'
        self.registerGlyph('uni207F')
        return True


    def checkAlphas(self):
        error = False
        for c in ABC_UC + ABC_LC:
            glyph = self.getGlyph(c)
            if glyph is None:
                error = True
                log('Missing glyph: ' + c)
            self.registerGlyph(c)

        supn = self.checkNsup()
        if supn is False:
            error = True

        if error is True:
            log('Please add missing glyphs. Exiting...')


    def checkDiacritics(self, checkCaps=True, checkSmcp=False):
        sufComb = lambda x: (x[0], x[1], x[1] + 'comb')
        markDiacritics = list(map(sufComb, UNI_DIACRITICS))

        error = False
        for uni, mark, name in markDiacritics:
            found = self.checkExistsAndSetName(uni, name)
            if found is False:
                error = True
                log('Missing glyph: ' + hex(uni) + ' ' + name)
        if error:
            log('Please add missing glyphs. Exiting...')
            exit()

        if checkCaps:
            for uni, mark, name in markDiacritics:
                self.checkOrCreateAltAccent(uni, name, 'cap')

        if checkSmcp:
            for uni, mark, name in markDiacritics:
                self.checkOrCreateAltAccent(uni, name, self.scSuffix)


    def checkOrBuildAccentedUnicode(self):
        for uni, name in ACCENTED_CHARS:
            glyph = self.getGlyph(uni)
            if glyph is None:
                glyph = self.font.createChar(uni, name)
                glyph.build()
                log('Built accented glyph: ' + name)
            else:
                glyph.glyphname = name
                self.registerGlyph(name)


    def checkSmallCaps(self):
        self.alphaScGlyphs = {}
        suf = self.scSuffix
        errs = []
        for lc in 'abcdefghijklmnopqrstuvwxyz':
            lcSc = self.font.findEncodingSlot(lc + '.' + suf)
            ucSc = self.font.findEncodingSlot(lc.upper() + '.' + suf)
            if lcSc > -1:
                self.alphaScGlyphs[lc] = self.font[lcSc]
            elif ucSc > -1:
                self.alphaScGlyphs[lc] = self.font[ucSc]
            else:
                errs.append(lc + '.' + suf)
        if len(errs) > 0:
            log('Missing small caps letter forms for: ' + ' '.join(errs))
            log('Add missing small caps and re-run')
            exit()


    """
    Ligature glyphs
    """
    def createLigaLookup(self):
        self.addLookup(LIGA_LOOKUP, 'gsub_ligature', 'liga')
        self.addLookupSubtable(LIGA_LOOKUP, LIGA_SUBTABLE)
        self.addLookup(CCMP_LOOKUP, 'gsub_ligature', 'ccmp')
        self.addLookupSubtable(CCMP_LOOKUP, CCMP_SUBTABLE)


    def buildLigatureGlyph(self, liga, base, mark):
        ligaGlyph = self.font.createChar(-1, liga)
        self.copyRefTo(base, ligaGlyph)

        if M_DOTA in mark:
            x_offset = ligaGlyph.width
            y_offset = 0
            x_offset += self.italicOffsetBetweenGlyphs(ligaGlyph, self.getGlyph(mark))
            ligaGlyph.addReference(mark, [1, 0, 0, 1, x_offset, y_offset])
        elif M_DIAB in mark:
            x_offset = self.centerX(ligaGlyph) - self.centerX(mark)
            y_offset = 0
            x_offset -= self.italicOffsetBetweenGlyphs(self.getGlyph(mark), ligaGlyph)
            ligaGlyph.addReference(mark, [1, 0, 0, 1, x_offset, y_offset])
        else:
            ligaGlyph.appendAccent(mark)

        self.registerGlyph(liga)
        return ligaGlyph


    def buildPOJligas(self):
        self.createLigaLookup()

        for name, base, mark, lookups in LIGA_SET:
            if base == 'i':
                base = DTLS_I[1]

            ligaGlyph = self.buildLigatureGlyph(name, base, mark)
            # Add the ligatures to the lookup tables
            for lookup in lookups:
                ligaGlyph.addPosSub(LIGA_SUBTABLE, lookup)
                ligaGlyph.addPosSub(CCMP_SUBTABLE, lookup)


    """
    base2mark anchors
    """
    def addMarkLookup(self):
        if MARK_LOOKUP not in self.font.gpos_lookups:
            self.addLookup(MARK_LOOKUP, 'gpos_mark2base', 'mark')


    def addPOJanchors(self):
        SPACING = 40
        # Add relevant lookup tables and subtables for mark2base
        self.addMarkLookup()
        self.addLookupSubtable(MARK_LOOKUP, MARK_TOP_CNTR)
        self.font.addAnchorClass(MARK_TOP_CNTR, ANCH_TOP)

        # Set mark anchors on tone diacritics
        for name in TONE_MARKS_COMB:
            glyph = self.getGlyph(name)
            xpos = self.centerX(glyph)
            ypos = glyph.boundingBox()[1]
            xpos += self.italicOffsetFromGlyphMid(glyph, ypos)
            glyph.addAnchorPoint(ANCH_TOP, 'mark', xpos, ypos)

        # Set base anchors on all alphabets
        for name in list(ABC_UC + ABC_LC) + ['dotlessi', 'dotlessj']:
            if name == 'dotlessj' and not self.hasDotlessj():
                continue

            glyph = self.getGlyph(name)
            xpos = self.centerX(glyph)
            ypos = glyph.boundingBox()[3] + SPACING
            xpos += self.italicOffsetFromGlyphMid(glyph, ypos)
            glyph.addAnchorPoint(ANCH_TOP, 'base', xpos, ypos)


    def addDotMarkAnchor(self):
        """Set base anchor in center of 'combining dot above right' uni0358
        """
        glyph = self.getGlyph(M_DOTA + 'comb')
        bounds = glyph.boundingBox()
        xpos = round((bounds[2] + bounds[0]) / 2)
        ypos = round((bounds[3] + bounds[1]) / 2)
        glyph.addAnchorPoint(ANCH_TOP_RIGHT, 'mark', xpos, ypos)


    def addDotBaseAnchors(self):
        vxy = self.vowelDotXY

        # Add anchors to all vowel classes
        for name in DOT_ANCHOR_SET:
            glyph = self.getGlyph(name)
            if vxy is not None:
                # User given coordinates
                x_i = 'AEIOUaeiou'.index(name[0]) * 2
                xpos = vxy[x_i]
                ypos = vxy[x_i + 1]
            else:
                # Automated coordinates from glyph bounds
                bounds = (self.getGlyph('dotlessi') if name[0] == 'i' else self.getGlyph(name[0])).boundingBox()
                xpos = bounds[2]
                ypos = bounds[3]
            glyph.addAnchorPoint(ANCH_TOP_RIGHT, 'base', xpos, ypos)


    def addDotAnchors(self):
        self.addMarkLookup()
        self.addLookupSubtable(MARK_LOOKUP, MARK_TOP_RIGHT)
        self.font.addAnchorClass(MARK_TOP_RIGHT, ANCH_TOP_RIGHT)
        self.addDotMarkAnchor()
        self.addDotBaseAnchors()


    def addSubDotlessIJLookups(self):
        """
        Adds a Single Substitution lookup, substituting
           i for dotlessi
           j for dotlessj (if it exists in the font)

        Adds a Contextual Chaining Substitution lookup
        to replace i and j when followed by a combining tone
        """
        self.addLookup(DTLS_LOOKUP, 'gsub_single', 'dtls')
        self.addLookupSubtable(DTLS_LOOKUP, DTLS_SUBTABLE)
        self.getGlyph('i').addPosSub(DTLS_SUBTABLE, 'dotlessi')

        if self.hasDotlessj():
            self.getGlyph('j').addPosSub(DTLS_SUBTABLE, 'dotlessj')

        self.addLookup(CCMP_DTLS, 'gsub_contextchain', 'ccmp')
        marks = ' '.join(TONE_MARKS_COMB)
        dotlesschars = '[i j]' if self.hasDotlessj() else '[i]'
        self.font.addContextualSubtable(
            CCMP_DTLS,
            CCMP_DTLS_SUBT,
            'coverage',
            dotlesschars + ' @<' + DTLS_LOOKUP + '> | [' + marks + ']'
        )

    """
    SmallCaps
    """
    def addSmallCapsLookups(self):
        """
        Will use an existing smallcaps lookup if found, otherwise creates a new one
        Creates both 'smcp' (lower > upper) and 'c2sc' (upper > lower) lookups
        """
        smcpLookup = None
        c2scLookup = None
        for lookup in self.font.gsub_lookups:
            info = self.font.getLookupInfo(lookup)
            if info[0] == 'gsub_single':
                if len(info[2]) > 0:
                    if info[2][0][0] == 'smcp' and smcpLookup is None:
                        smcpLookup = lookup
                    elif info[2][0][0] == 'c2sc' and c2scLookup is None:
                        c2scLookup = lookup

        if smcpLookup is None:
            lastLookup = self.font.gsub_lookups[len(self.font.gsub_lookups) - 1]
            self.addLookup(SMCP_LOOKUP, 'gsub_single', 'smcp', lastLookup)
            smcpLookup = SMCP_LOOKUP

        if c2scLookup is None:
            self.addLookup(C2SC_LOOKUP, 'gsub_single', 'c2sc', smcpLookup)
            c2scLookup = C2SC_LOOKUP

        self.addLookupSubtable(smcpLookup, SMCP_SUBT)
        self.addLookupSubtable(c2scLookup, C2SC_SUBT)

    def getSmallCapsBuildList(self):
        """
        Check which accented small caps characters already in font
        return a list of those which need to be built
        (does not include the o_dotaboveright and u_diaresisbelow characters,
        which are assumed to be not included in any normal font)
        """
        suf = self.scSuffix
        bases = 'aeimnou'
        toBuild = []
        for base in bases:
            for mark in TONE_MARKS:
                nameUC = getAccentedCharName(base.upper(), mark)
                nameLC = getAccentedCharName(base, mark)
                names = []
                for n in [nameUC, nameLC]:
                    names.append(n)
                    if '_' not in n:
                        names.append(uni_name_from_int(self.getGlyph(n).unicode))
                found = False
                for name in names:
                    glyph = self.getGlyph(f'{name}.{suf}')
                    if glyph is not None:
                        found = True
                        break
                if found is False:
                    nameSC = f'{nameLC}.{suf}'
                    toBuild.append((nameLC, nameUC, nameSC, base, f'{mark}comb.{suf}'))

        for base, mod in [('o', M_DOTA), ('u', M_DIAB)]:
            for tone in [''] + TONE_MARKS:
                nameLC = getAccentedCharName(base, tone)
                nameUC = getAccentedCharName(base.upper(), tone)
                baseChar = f'{nameLC}.{suf}'
                if base == 'u' and tone == '':
                    nameLC += mod
                    nameUC += mod
                    nameSC = f'{nameLC}{mod}.{suf}'
                else:
                    nameLC += '_' + mod
                    nameUC += '_' + mod
                    nameSC = f'{nameLC}.{suf}'
                toBuild.append((nameLC, nameUC, nameSC, baseChar,  f'{mod}comb.{suf}'))
        return toBuild


    def buildSmallCaps(self):
        """
        Build all missing accented small caps. Prior to running, ensure that:
        - Small capitals for base letters A-Z exist:
            a.sc, b.sc, c.sc, ... (or A.sc, B.sc, C.sc, ...)
        - smcp accents exist:
            acutecomb.sc, gravecomb.sc, ...
        - Existing smallcaps characters will be skipped if their name matches one of:
            e.g., for smallcaps Á: aacute.sc, Aacute.sc, uni00C1.sc, uni00E1.sc
            These will not be added to the POJ smcp lookup tables
        """
        self.checkSmallCaps()
        self.addSmallCapsLookups()

        alphaScGlyphs = self.alphaScGlyphs
        suf = self.scSuffix
        toBuild = self.getSmallCapsBuildList()

        for nameLC, nameUC, nameSC, base, mark in toBuild:
            if base in alphaScGlyphs:
                base = alphaScGlyphs[base].glyphname
            self.buildLigatureGlyph(nameSC, base, mark)
            self.getGlyph(nameLC).addPosSub(SMCP_SUBT, nameSC)
            self.getGlyph(nameSC).addPosSub(C2SC_SUBT, nameSC)


    """
    Kerning
    """
    def autoKern(self, separation=200, class_distance=20):
        """
        Attemps to build UC>LC and LC>UC kerning
        """
        KERN_LOOKUP = "'kern' POJ kerning"
        KERN_UL_SUBTABLE = f'{KERN_LOOKUP} POJ uppers-lowers'
        KERN_LU_SUBTABLE = f'{KERN_LOOKUP} POJ lowers-uppers'
        self.addLookup(KERN_LOOKUP, 'gpos_pair', 'kern')

        glyphList = filter(lambda x: f'.{self.scSuffix}' not in x, self.glyphList)
        uppers = []
        lowers = []
        for name in glyphList:
            if name[0].isupper():
                uppers.append(self.getGlyph(name))
            else:
                lowers.append(self.getGlyph(name))

        self.font.addKerningClass(KERN_LOOKUP, KERN_UL_SUBTABLE, separation, class_distance, uppers, lowers, True)
        self.font.addKerningClass(KERN_LOOKUP, KERN_LU_SUBTABLE, separation, class_distance, lowers, uppers, True)


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
            '        name    diacritic\n'
            '        uni0300 COMBINING GRAVE ACCENT\n'
            '        uni0301 COMBINING ACUTE ACCENT\n'
            '        uni0302 COMBINING CIRCUMFLEX ACCENT\n'
            '        uni0304 COMBINING MACRON\n'
            '        uni0306 COMBINING BREVE\n'
            '        uni030A COMBINING RING ABOVE\n'
            '        uni030B COMBINING DOUBLE ACUTE ACCENT (HUNGARIAN UMLAUT)\n'
            '        uni030C COMBINING CARON\n'
            '        uni030D COMBINING VERTICAL LINE ABOVE\n'
            '        uni0324 COMBINING DIAERESIS BELOW\n'
            '        uni0358 COMBINING DOT ABOVE RIGHT\n\n'
            ' - uppercase versions of above, named with `.cap` suffix\n'
            ' - all diacritics should be centered in a zero-width glyph\n'
            ' - dotlessi (U+0131) is required, dotlessj (U+0237) is optional\n\n'
            'Example: ffpython build_poj.py --input MyFont.sfd \\\n'
            '                               --output poj-JiKut.sfd \\\n'
            '                               --vxy 500 527 587 658 339 707 647 667 713 720 \\   # uppercase AEIOU\n'
            '                                     431 417 450 432 272 366 496 448 473 505     # lowercase aeiou')
    parser = ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', '--input', type=str, required=True, help='The input .sfd font file')
    parser.add_argument('-o', '--output', type=str, default='output.sfd', help='The output .sfd font file (default: output.sfd)')
    parser.add_argument('--vowel-dots', type=int, nargs=20, metavar=('Ax', 'Ay', 'Ex', 'Ey', 'Ix', 'Iy', 'Ox', 'Oy', 'Ux', 'Uy', 'ax', 'ay', 'ex', 'ey', 'ix', 'iy', 'ox', 'oy', 'ux', 'uy'), help='XY-coords for dots next to vowels AEIOUaeiou [Ax Ay...ux uy]')
    parser.add_argument('--skip-dotlessi', action='store_true', help='Do not replace ij with dotlessij')
    parser.add_argument('--skip-poj-anchors', action='store_true', help='Do not add top center anchors')
    parser.add_argument('--skip-dot-anchors', action='store_true', help='Do not add dot anchors')
    parser.add_argument('--skip-ligas', action='store_true', help='Do not build POJ ligatures')
    parser.add_argument('--sc-suffix', type=str, metavar='SUFFIX', help='suffix for SmallCaps (e.g., sc)')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--auto-kern', action='store_true', help='Attempt to autokern POJ glyphs')
    group.add_argument('--kern-sep', type=int, nargs=2, metavar=('SEPARATION', 'SIMILARITY'), help='Specify the separation and class-similarity (1-20) parameters')

    args = parser.parse_args()

    f1 = POJFont(args.input)
    f1.run(args)
