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
        var parent = $(this).parent();
        var nested = parent.find('.nested');
        nested.toggleClass('active');
        $(this).toggleClass('caret-down');
    });
});
