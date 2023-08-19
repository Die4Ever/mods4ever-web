function RenderLeaderboard(parent, leaderboard) {
    table = $('<table>');
    row = $('<tr>');
    row.append($('<th>Place</th><th>Name</th><th>Score</th><th>Time</th>'));
    table.append(row);
    for(var i=0; i<leaderboard.length; i++) {
        row = RenderRun(leaderboard[i]);
        table.append(row);
    }
    parent.append(table);
}

function FormatTime(time) {
    var total_seconds = time/10;
    var hours = Math.floor(total_seconds/3600);
    var remaining = total_seconds - hours*3600;
    var minutes = Math.floor(remaining/60);
    var seconds = total_seconds - hours*3600 - minutes*60;

    return hours+'h ' + minutes.toString().padStart(2, '0')+'m ' + seconds.toFixed(1)+'s';
}

function RenderRun(run) {
    row = $('<tr>');
    row.append($(
        '<td>#'+run['place']+'</td>'
        +'<td>'+run['name']+'</td>'
        +'<td>'+run['score']+'</td>'
        +'<td>'+FormatTime(run['time'])+'</td>'
    ));
    row.attr('title', JSON.stringify(run));
    return row;
}

function pauseYoutube(el) {
    el.each(function() {
        jQuery(this)[0].contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*')
    });
}

$(function() {
    $('.caret').click(function(e) {
        var id = $(this)[0].id;
        history.pushState({}, '', '#'+id);
        var li = $(this).parent();
        var ul = li.parent();
        var nested = li.find('.nested');
        if(nested.hasClass('active')) {
            nested.removeClass('active');
            $(this).removeClass('caret-down');
            pauseYoutube(nested.find("iframe"));
        } else {
            var actives = ul.find('> li > .active');
            actives.removeClass('active');
            pauseYoutube(actives.find("iframe"));
            var carets = ul.find('> li > .caret-down');
            carets.removeClass('caret-down');

            nested.addClass('active');
            $(this).addClass('caret-down');
        }
        return false;
    });

    if(location.hash.length > 1) {
        var el = $(location.hash);
        if(el.hasClass('caret')) {
            el.click();
        }
    }
});
