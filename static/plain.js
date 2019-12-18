function processDelete(resp) {
    if(resp.error) {
        alert('Error: ' + resp.error);
    }
    var aid = resp.aid;
    $("[data-aid='"+aid+"']").remove();
};

$("#availabilities").on('click', '.deleteAvailability', function(event){
    if (event.target != this) return;
    var aid = $(this).closest("[data-aid").attr("data-aid");

    $.post(url, {'aid': aid}, processDelete);
});