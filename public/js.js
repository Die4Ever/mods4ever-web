function RenderLeaderboard(parent, leaderboard) {
    table = $('<table>');
    row = $('<tr>');
    row.append($('<th>Place</th><th>Name</th><th>Score</th>'));
    table.append(row);
    for(var i=0; i<leaderboard.length; i++) {
        row = RenderRun(leaderboard[i]);
        table.append(row);
    }
    parent.append(table);
}

function RenderRun(run) {
    row = $('<tr>');
    row.append($(
        '<td>#'+run['place']+'</td>'
        +'<td>'+run['name']+'</td>'
        +'<td>'+run['score']+'</td>'
    ));
    row.attr('title', JSON.stringify(run));
    return row;
}

$(function() {
    $('.caret').click(function(e) {
        var li = $(this).parent();
        var ul = li.parent();
        var nested = li.find('.nested');
        if(nested.hasClass('active')) {
            nested.removeClass('active');
            $(this).removeClass('caret-down');
        } else {
            var actives = ul.find('> li > .active');
            actives.removeClass('active');
            var carets = ul.find('> li > .caret-down');
            carets.removeClass('caret-down');

            nested.addClass('active');
            $(this).addClass('caret-down');
        }
        return false;
    });
});
