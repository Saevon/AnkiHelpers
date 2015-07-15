kanji = "要 超 争 宅 定 即 星 簡 探 戦 第 撮 熱 節 係 惑 恐 関 巻 絡 章 季 句 諦 恩 否 深 乳 偵 迷 系 険";

function openTab(url){
    var a = document.createElement("a");
    a.href = url;
    var evt = document.createEvent("MouseEvents");
    evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, true, 0, null);
    a.dispatchEvent(evt);
}

kanji_list = kanji.split(" ");
/*
for (i=0; i < kanji_list.length; i++) {
  openTab("http://jisho.org/words?jap=＊" + kanji_list[i] + "＊&eng=&dict=edict&common=on");
}
*/

for (i=0; i < kanji_list.length; i++) {
  openTab("http://www.kanjidamage.com/kanji/search?utf8=%E2%9C%93&q=" + kanji_list[i]);
}
