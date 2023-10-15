function LoadLeaderboard() {
    const urlParams = new URLSearchParams(window.location.search);
    const SortBy = urlParams.get('SortBy');
    const Grouped = urlParams.get('Grouped');

    $.getJSON( "/api/dxrando/leaderboard?SortBy="+SortBy+"&Grouped="+Grouped, function( r ) {
        var el = $('.leaderboard');
        el.html('');
        RenderLeaderboard(el, r);
    });
}

function RenderLeaderboard(parent, leaderboard) {
    table = $('<table>');
    row = $('<tr>');
    row.append($(
        '<th>Place</th><th>Name</th>'
        + '<th><a href="?SortBy=score">Score</a></th>'
        + '<th><a href="?SortBy=totaltime">Time</a></th>'
        + '<th>Flags</th>'
    ));
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
        +'<td>'+FormatTime(run['totaltime'])+'</td>'
        +'<td>'+run['flagshash']+'</td>'
    ));
    row.attr('title', JSON.stringify(run));
    return row;
}

function pauseYoutube(el) {
    el.each(function() {
        jQuery(this)[0].contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*')
    });
}

function toggleSection(el) {
    var id = el[0].id;
    var hash = '#'+ id.replace(/^proj/, '');
    history.pushState({}, '', hash);

    var li = el.parent();
    var ul = li.parent();
    var nested = li.find('.nested');
    if(nested.hasClass('active')) {
        nested.removeClass('active');
        el.removeClass('caret-down');
        pauseYoutube(nested.find("iframe"));
    } else {
        var actives = ul.find('> li > .active');
        actives.removeClass('active');
        pauseYoutube(actives.find("iframe"));
        var carets = ul.find('> li > .caret-down');
        carets.removeClass('caret-down');

        nested.addClass('active');
        el.addClass('caret-down');
    }
}

function isMobile() {
    return $('.content').css('max-width') === 'none';
}

$(function() {
    $('.caret').click(function(e) {
        if(isMobile()) {
            return true;// use the regular link for mobile
        }
        toggleSection($(this));
        return false;
    });

    var hash = location.hash;
    if(hash) {
        hash = hash.replace('#', '#proj');
        var el = $(hash);
        if(el && el.hasClass('caret')) {
            toggleSection(el);
        }
    }
});
