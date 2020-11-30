# Iōng chū-tōng-hòa kang-kū chò Pe̍h-ōe-jī jī-thé

Chit-phiⁿ bûn-kiāⁿ ē soeh-bêng án-chóaⁿ sú-iōng A-ióng chò ê Python script lâi chò Pe̍h-ōe-jī jī-thé. Lí nā-sī m̄-chai-iáⁿ án-chóaⁿ iōng python script, ē-tàng chham-khó ti̍t-chiap iōng Fontforge chò jī-thé ê soeh-bêng: [Chò-hóe lâi chò Pe̍h-ōe-jī jī-thé](lets-make-POJ-font.md)

# 用自動化工具做白話字字體

這篇文件會說明按怎使用阿勇做 ê python script 來做白話字字體。你若是毋知影按怎用 Python script，會當參考直接用 Fontforge 做字體 ê 說明：[做夥來做白話字字體](lets-make-POJ-font.md)


## 1. Siat-tēng khoân-kéng kah nńg-thé

* An-chng [FontForge](https://fontforge.org/en-US/)
* Ài ū pán-pún > 3 ê Python, pēng-chhiáⁿ an-chng `fontforge` module  
    
    * Nā-sī Windows, ē-tàng ti̍t-chiap sú-iōng FontForge an-chng ê chu-liāu-a̍p-á lāi-té ê `fontforge-console.bat` (e.g., `C:\Program Files (x86)\FontForgeBuilds\fontforge-console.bat`) ê Terminal, m̄-bián lēng-gōa chng module.
    * Mā ē-sái iōng `pip install python-fontforge` lâi chng module
    * Nā-sī Mac OS, góa chhì-kòe ū-hāu ê sī 
      ```
      brew install fontforge
      brew link fontforge
      ```
* Táng-ló͘ project ê tóng-àn, chhōe-tio̍h `POJFonts/src/poj.py` ê lō͘-kèng.

  Nā-sī lóng ū chng hó, ē-tàng chip-hêng `poj.py -h` lâi khòaⁿ chit ki script thê-kiong ê kong-lêng kah chí-lēng soeh-bêng. Chip-hêng ē-sái iōng:
  ```
  python /path/to/poj.py -h
  ```
  iá-sī:
  ```
  ffpython /path/to/poj.py -h
  ```

## 1. 設定環境佮軟體
* 安裝 [FontForge](https://fontforge.org/en-US/)
* 愛有版本 > 3 ê Python, 並且安裝 `fontforge` module  
    
    * 若是 Windows, 會當直接使用 FontForge 安裝 ê 資料匣仔內底 ê `fontforge-console.bat` (e.g., `C:\Program Files (x86)\FontForgeBuilds\fontforge-console.bat`) ê Terminal, 毋免另外裝 module。
    * 嘛會使用 `pip install python-fontforge` 來裝 module
    * 若是 Mac OS，我試過有效 ê 是 
      ```
      brew install fontforge
      brew link fontforge
      ```

* Táng-ló͘ project ê 檔案，揣著 `POJFonts/src/poj.py` ê 路徑。

  若是攏有裝好，會當執行 `poj.py -h` 來看這支 script 提供 ê 功能佮指令說明。執行會使用：
  ```
  python /path/to/poj.py -h
  ```
  iá-sī:
  ```
  ffpython /path/to/poj.py -h
  ```


## 2. Chún-pī jī-bó kah hû-hō
Tī chip-hêng `poj.py -h` liáu-āu ē khòaⁿ-tio̍h chin-chē chit-ki script ē-tàng án-chóaⁿ sú-iōng kah tiâu-chéng ê hong-hoat. Tān-sī beh khai-sí chìn-chêng ài seng kā jī-thé ê tóng-àn choán chò `.sfd` ê kek-sek. Chí-iàu tī FontForge phah-khui jī-thé, "File" > "Save" chhûn chò `.sfd` pán-pún ê tō ē-sái.  

koh-lâi chip-hêng 
```
python /path/to/poj.py -i /path/to/font-file.sfd
```

Terminal lāi-té ē hián-sī oân-sêng chit-ê jī-thé su-iàu ê jī-bó kah hû-hō. 

## 2. 準備字母佮符號
佇執行 `poj.py -h` 了後會看著真濟這支 script 會當按怎使用佮調整 ê 方法。但是欲開始進前愛先共字體 ê 檔案轉做 `.sfd` ê 格式。只要佇 FontForge 拍開字體， "File" > "Save" 存做 `.sfd` 版本 ê 就會使。

閣來執行
```
python /path/to/poj.py -i /path/to/font-file.sfd
```
Terminal 內底會顯示完成這个字體需要 ê 字母佮符號。


### A. Jī-bó
Ki-pún-siōng thêng-sek chip-hêng í-āu èng-kai lóng ē khòaⁿ-tio̍h:
```
Missing superscript n (uni207F)
```
Tō-sī su-iàu pó͘ chò "ⁿ" ê ì-sù. Nā-sī m̄-chai-iáⁿ beh án-chóaⁿ chò, ē-tàng chham-khó [Chò-hóe lâi chò Pe̍h-ōe-jī jī-thé](lets-make-POJ-font.md) lāi-té "4. Khai-sí chò jī pó͘ jī" ê "Hoān-lē 1".

Lēng-gōa chi̍t-ê khah khó-lêng khiàm ê jī-bó sī 
```
uni0131 LATIN SMALL LETTER DOTLESS I (dotlessi, ı)
```
Ē-sái the̍h phó͘-thong ê "i" lâi chò.

### A. 字母
基本上程式執行以後應該攏會看著：
```
Missing superscript n (uni207F)
```
就是需要補做 "ⁿ" ê 意思。若是毋知影欲按怎做，會當參考 [做夥來做白話字字體](lets-make-POJ-font.md) 內底 「4. 開始做字補字」 ê 「範例 1」。

另外一个較可能欠 ê 字母是
```
uni0131 LATIN SMALL LETTER DOTLESS I (dotlessi, ı)
```
會使提普通 ê "i" 來做。


### B. Hû-hō
Khó-lêng su-iàu pó͘ ê hû-hō ū chit-kóa:
```
name     diacritic
uni0300  COMBINING GRAVE ACCENT         siaⁿ-tiāu 3
uni0301  COMBINING ACUTE ACCENT         siaⁿ-tiāu 2
uni0302  COMBINING CIRCUMFLEX ACCENT    siaⁿ-tiāu 5
uni0304  COMBINING MACRON               siaⁿ-tiāu 7
uni0306  COMBINING BREVE                siaⁿ-tiāu 9
uni030A  COMBINING RING ABOVE           Pha̍k-fa-sṳ (Kheh-ōe ê siaⁿ-tiāu)
uni030B  COMBINING DOUBLE ACUTE ACCENT  siaⁿ-tiāu 9 (Kàu-io̍k-pō͘)
uni030C  COMBINING CARON                siaⁿ-tiāu 6 (Hái-kháu-khiuⁿ)
uni030D  COMBINING VERTICAL LINE ABOVE  siaⁿ-tiāu 8
uni0324  COMBINING DIAERESIS BELOW      Pha̍k-fa-sṳ (Kheh-ōe ê siaⁿ-tiāu), Hái-kháu-khiuⁿ
uni0358  COMBINING DOT ABOVE RIGHT      o͘ téng-koân ê tiám
```

Ē-sái ùi í-keng ū ê jī lāi-té chhōe khòaⁿ ū tú-á-hó ē-tàng lī-iōng ê pō͘-hūn bô. Chò hó ài 
tī keh-á téng-koân chiàⁿ-ji̍h, soán "Glyph Info". Tī phah-khui ê thang-á lāi-té chhōe-tio̍h "Unicode Value", su-li̍p tùi-èng ê Unicode the̍h-tiāu "uni" ê pō͘-hūn (chhiūⁿ siaⁿ-tiāu 3 ê `uni0300` tō ài su-li̍p `0300`), Name tō ti̍t-chiap siá téng-koân lia̍t ê. Koh-lâi ji̍h siōng ē-kha ê "OK" kā thang-á koaiⁿ-tiāu.  

Leh chò ê sî-chūn ē-tàng khǹg ē tàu chò-hóe sú-iōng ê jī-bó li̍p-khì chò tiâu-chéng ūi-tì ê chham-khó. Lēng-gōa mā ē-sái tī im-tiāu hû-hō ê keh-á téng-koân chiàⁿ-ji̍h, tiám "Center in Width", án-ne leh kah jī-bó cho͘-ha̍p ê sî-chūn khah bē cháu siuⁿ hn̄g.

### B. 符號
可能需要補 ê 符號有這寡：
```
name     diacritic
uni0300  COMBINING GRAVE ACCENT         聲調 3
uni0301  COMBINING ACUTE ACCENT         聲調 2
uni0302  COMBINING CIRCUMFLEX ACCENT    聲調 5
uni0304  COMBINING MACRON               聲調 7
uni0306  COMBINING BREVE                聲調 9
uni030A  COMBINING RING ABOVE           Pha̍k-fa-sṳ (客話 ê 聲調)
uni030B  COMBINING DOUBLE ACUTE ACCENT  聲調 9 (教育部)
uni030C  COMBINING CARON                聲調 6 (海口腔)
uni030D  COMBINING VERTICAL LINE ABOVE  聲調 8
uni0324  COMBINING DIAERESIS BELOW      Pha̍k-fa-sṳ (客話 ê 聲調), 海口腔
uni0358  COMBINING DOT ABOVE RIGHT      o͘ 頂懸 ê 點
```

會使對已經有 ê 字內底揣看有拄仔好會當利用ê部份無。做好愛佇格仔頂懸正揤，選 "Glyph Info"。佇拍開 ê 窗仔內底揣著 "Unicode Value"， 輸入對應 ê Unicode 提掉 "uni" ê 部份（像聲調 3 ê `uni0300` 就愛輸入 `0300`），Name 就直接寫頂懸列 ê 。閣來揤上下跤 ê "OK" 共窗仔關掉。

咧做 ê 時陣會當囥會鬥做伙使用 ê 字母入去做調整位置 ê 參考。另外嘛會使佇音調符號 ê 格仔頂懸正揤，點 "Center in Width"，按呢咧佮字母組合 ê 時陣較袂走傷遠。


### C. Tōa-sió-siá ê siaⁿ-tiāu hû-hō
In-ūi tōa-sió-siá jī-bó ê koân-tō͘ bô-kâng, nā-sī lóng iōng kâng chi̍t thò siaⁿ-tiāu hû-hō lâi cho͘-ha̍p, khó-lêng ē ū chi̍t-kóa jī-bó su-iàu koh tiâu-chéng. Só͘-í sui-liân bô hān-chè it-tēng ài chò, mā-sī kiàn-gī chiam-tùi tōa-siá jī-bó chò bô-kâng ê siaⁿ-tiāu hû-hō. Chò ê sî-chūn Unicode lóng siat-tēng `-1`, Name ê só͘-chāi tō kā goân-lâi ê Name āu-piah ka `.cap`, chhin-chhiūⁿ hō͘ tōa-siá iōng ê siaⁿ-tiāu 3 i ê Name tō ē hō chò `uni0300.cap`. It-poaⁿ lāi-kong tōa-siá jī-bó iōng ê siaⁿ-tiāu hû-hō koân-tō͘ ē khah é, án-ne tōa-siá jī-bó ka-siōng hû-hō chiah bē siūⁿ koân. Nā-sī beh lēng-gōa chò ê sī sió-siá jī-bó iōng ê siaⁿ-tiāu hû-hō, Name ê āu-piah ài kái ka `.sc`.

### C. 大小寫 ê 聲調符號
因為大小寫字母 ê 懸度無仝，若是攏用仝一套聲調符號來組合，可能會有一寡字母需要閣調整。所以雖然無限制一定愛做，嘛是建議針對大寫字母做無仝 ê 聲調符號。做 ê 時陣 Unicode 攏設定 `-1`， Name ê 所在就共原來ê Name 後壁加 `.cap`，親像予大寫用 ê 聲調 3 伊 ê Name 就會號做 `uni0300.cap`。一般來講大寫字母用 ê 聲調符號懸度會較矮，按呢大寫字母加上符號才袂傷懸。若是欲另外做 ê 是小寫字母用 ê 聲調符號， Name ê 後壁愛改加 `.sc`。


### D. Ka tiám ê E, I kah U
Tû liáu O͘ í-gōa, mā ū lâng sú-iōng ka tiám ê E, I kah U lâi piáu-hiān in ê khiuⁿ-kháu. Chit-ê pō͘-hūn ū pau-koat tī Lookups ê `mark2base` lāi-té. Mā ē-sái iōng `--skip-dot-anchors` kā koaiⁿ-tiāu. Nā-sī ū beh chò chit-kóa jī (kiàn-gī ài chò), chip-hêng chi̍t-pái chit-ê script í-āu, tō ài khì Lookups ê `mark2base` thang-á tiâu-chéng tiám beh khǹg ê ūi. `A` mā tī lāi-té sī beh hō͘ in khòaⁿ--khí-lâi khah oân-chéng. Siông-sè ê hong-hoat:

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

Koh-lâi, tī tò-pêng soán beh tiâu-chéng ê jī-bó, kā nâ-sek ê "+" kì-hō thoa káu siūⁿ-beh khǹg tiám ê ūi, khòaⁿ ū sek-ha̍p bô. Nā-sī ē-sái, tō kā tò-pêng X kah Y chō-phiau ê sò͘-jī kì--khí-lâi. Kā `A E I O U a e i o u` lóng tiâu-chéng liáu í-āu, ài kā chit-kóa sò͘-jī iōng `--vowel-dots` chiàu sūn-sū thoân hō͘ script. Chhiūⁿ án-ne:

```
--vowel-dots 500 527 587 658 339 707 647 667 713 720 431 417 450 432 272 366 496 448 473 505
# Téng-koân ê sò͘-jī hun-pia̍t piáu-sī bô-kâng jī-bó ê tiám ê X, Y chō-phiau sò͘-jī:
#            Ax  Ay  Ex  Ey  Ix  Iy  Ox  Oy  Ux  Uy  ax  ay  ex  ey  ix  iy  ox  oy  ux  uy
```

### D. 加點 ê E, I 佮 U
除了 O͘ 以外，嘛有人使用加點 ê E, I 佮 U 來表現 in ê 腔口。這个部份有包括佇 Lookups ê `mark2base` 內底。嘛會使用 `--skip-dot-anchors` 共關掉。若是有欲做這寡字（建議愛做），執行一擺這个 script 以後，就愛去 Lookups ê `mark2base` 窗仔調整點欲囥 ê 位。`A` 嘛佇內底是欲予 in 看起來較完整。詳細 ê 方法：

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

閣來，佇倒爿選欲調整 ê 字母，共藍色 ê "+" 記號拖到想欲囥點 ê 位，看有適合無。若是會使，就共倒爿 X 佮 Y 座標 ê 數字記起來。共 `A E I O U a e i o u` 攏調整了以後，愛共這寡數字用 `--vowel-dots` 照順序傳予 script。 像按呢：

```
--vowel-dots 500 527 587 658 339 707 647 667 713 720 431 417 450 432 272 366 496 448 473 505
# 頂懸 ê 數字分別表示無仝字母 ê 點 ê X, Y 座標數字：
#            Ax  Ay  Ex  Ey  Ix  Iy  Ox  Oy  Ux  Uy  ax  ay  ex  ey  ix  iy  ox  oy  ux  uy
```


### E. Chū-tōng tiâu-chéng jī kan ê khang-khiah (Kerning)
Ū-tang-sî-á ū chi̍t-kóa jī khǹg chò-hóe ê sî-chūn su-iàu tiâu-chéng nn̄g jī chi-kan ê khang-khiah, chhiūⁿ `Tn`. Khang-khiah ê tōa-sè ē-sái iōng `--auto-kern` chū-tōng tiâu-chéng, ia̍h-sī iōng `--kern-sep` ka-kī chí-tēng. `--kern-sep` su-iàu nn̄g ê sò͘-jī:

1. Khang-khiah hun-khui ê kī-lî (e.g., 100)
2. Nn̄g jī sio óa ê thêng-tō͘ (1 sī nn̄g ê tú-á-hó kheh chò-hóe, 20 sī sang-sang, ē-tàng tiâu-chéng khòaⁿ kî-tha sò͘-jī ê hāu-kó)
   
Bô te̍k-pia̍t chí-tēng ê sî-chūn tō-sī sú-iōng `--auto-kern`, hāu-kó kah `--kern-sep 200 20` sio-kāng.

### E. 自動調整字間 ê 空隙（Kerning）
有當時仔有一寡字囥做伙 ê 時陣需要調整兩字之間 ê 空隙，像 `Tn`。空隙 ê 大細會使用 `--auto-kern` 自動調整，猶是用 `--kern-sep` 家己指定。 `--kern-sep` 需要兩个數字：

1. 空隙分開 ê 距離 (e.g., 100)
2. 兩字相倚 ê 程度（ 1 是兩个字拄仔好𤲍做伙， 20 是鬆鬆，會當調整看其他數字 ê 效果）

無特別指定 ê 時陣就是使用 `--auto-kern`，效果佮 `--kern-sep 200 20` 相仝。


## 3. Tiâu-chéng
Tī thêng-sek chip-hêng liáu-āu, ài iōng FontForge phah-khui su-chhut ê tóng-àn (nā-sī bô chí-tēng, ē tī chu-liāu-a̍p-á lāi-té ê `output.sfd` ) kiám-cha thêng-sek tàu cho͘ chhut-lâi ê jī, tùi `uni00C0` kàu `uni01F9`, koh-ū siōng āu-piah bô tùi-èng ê Unicode ê jī-bó. Nā-sī siaⁿ-tiāu hû-hō ê ūi-tì khòaⁿ khí-lâi koài-koài, tō ài tiám li̍p-khì tiâu-chéng. Chhiūⁿ o͘ chit-khóan ka hû-hō í-āu khoah-tō͘ ū kái-piàn ê jī, ài khì "Metrics" > "Set Width" su-li̍p sin ê khoah-tō͘. Tī jī-bó lia̍t-pió ê ōe-bīn mā ē-sái "shift" ji̍h hō͘ tiâu nā iōng ku̍t-chhú soán siūⁿ beh kài ê jī, tō ē-sái chò chit-pái tiâu-chéng.

## 3. 調整
佇程式執行了後，愛用 FontForge 拍開輸出 ê 檔案（若是無指定，會佇資料匣仔內底 ê `output.sfd`）檢查程式鬥組出來 ê 字，對 `uni00C0` 到 `uni01F9`，閣有上後壁無對應 ê Unicode ê 字母。若是聲調符號 ê 位置看起來怪怪，就愛點入去調整。像 o͘ 這款加符號以後闊度有改變 ê 字，愛去 "Metrics" > "Set Width" 輸入新 ê 闊度。佇字母列表 ê 畫面嘛會使 "shift" 揤予牢那用滑鼠選想欲改 ê 字，就會使做一擺調整。


## 4. Hō miâ
Hō miâ ài chiàu sú-iōng ê jī-thé ê siū-khoân kui-tēng. Siu-kái chit-kóa khai-goân jī-thé (OFL Fonts) bē-sái koh sú-iōng kah goân-lâi kâng-khóan ê miâ, ài hō chi̍t-ê oân-choân sin--ê. "Element" > "Font Info..." tò-pêng soán "PS Names" kah miâ ū koan-hē ê só͘-chāi lóng ài kài, koh ū tò-pêng soán "TTF Names" ê lāi-iông mā-sī. 

## 4. 號名
號名愛照使用 ê 字體 ê 授權規定。修改這寡開源字體（OFL Fonts）袂使閣使用佮原來仝款 ê 名，愛號一个完全新--ê。"Element" > "Font Info..." 倒爿選 "PS Names" 佮名有關係 ê 所在攏愛改，閣有倒爿選 "TTF Names" ê 內容嘛是。


## 5. Su-chhut
Beh su-chhut ē-tàng an-chong ê jī-thé, "File" > "Generate Fonts..." soán hó tóng-àn beh khǹg ê só͘-chāi, tóng-miâ ē-kha soán soán `OpenType (CFF)`. Phah-khui "Options", ài kau `Hints`, `Flex Hints`, `PS Glyph Names`, `OpenType`, kî-tha ê lóng mài kau, ji̍h "OK" kā thang-á koaiⁿ-tiāu. Ji̍h "Generate", chò hó ê jī-thé tóng-àn tō ē chhut-hiān tī soán hó ê chu-liāu-a̍p-á lāi-té ah.

## 5. 輸出
欲輸出會當安裝 ê 字體， "File" > "Generate Fonts..." 選好檔案欲囥 ê 所在，檔名下跤選 `OpenType (CFF)`。拍開 "Options" 愛勾 `Hints`, `Flex Hints`, `PS Glyph Names`, `OpenType`，其他攏莫勾，揤 "OK" 共窗仔關掉。揤 "Generate"，做好 ê 字體檔案就會出現佇選好 ê 資料匣仔內底矣。