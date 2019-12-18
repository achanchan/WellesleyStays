function processDelete(resp) {
    if(resp.error) {
        alert('Error: ' + resp.error);
    }
    var aid = resp.aid;
    $("[data-aid='"+aid+"']").remove();
};

$("#availabilities").on('click', '.deleteAvailabilityAjax', function(event){
    if (!progressive_on) return;
    if (event.target != this) return;
    var aid = $(this).closest("[data-aid").attr("data-aid");

    $.post(deleteURL, {'aid': aid}, processDelete);
});