var jq = document.createElement('script');
jq.src = "https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js";
jq.onload = function() {
    jQuery.noConflict();
    console.log("Setup Complete");

    main();
};
document.getElementsByTagName('head')[0].appendChild(jq);


function to_kanji_damage(text) {
    return 'http://www.kanjidamage.com/kanji/search?utf8=%E2%9C%93&q=' + text;
}


// Creates a link to kanji damage from each kanji on the jisho site
function main() {
    $('.character').each(function(i, val) {
        var elem = $(val);

        elem.wrap('<a style="color: transparent;" target="_blank" href="' + to_kanji_damage(elem.text()) + '"></a>');
    });
}
