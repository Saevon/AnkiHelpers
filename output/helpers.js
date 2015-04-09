


function jlpt(levels) {
	var str = '';
	for (var i = levels.length - 1; i >= 0; i--) {
		str += ', .jlpt-n' + levels[i].toString();
	}

	return $(str);
}
