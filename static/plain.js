var url_to_delete = "{{url_for('deleteAvailabilityAjax')}}";

function processDelete(resp) {
    var aid = resp.aid;
    $("[data-aid="+aid+"]").remove();
};

$("#availabilities").on('click', '.deleteAvailability', function(event){
    if (event.target != this) return;
    var aid = $(this).closest("[data-aid").attr("data-aid");

    $.post(url_to_delete, {'aid': aid}, processDelete, 'json');
});