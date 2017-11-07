/* Javascript for SliceXBlock. */
function SliceXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    //Display to result
    function updateSlice(result) {
        $('.slices', element).text(result.video_id);
    }

    function updateThumbs(result) {
        $('.video_slices', element).text(result.video_slices);
    }


    var handlerUrl = runtime.handlerUrl(element, 'increment_count');
    var handlerVideoSlices = runtime.handlerUrl(element, 'generate_slices');
    var getVideoSlices = runtime.handlerUrl(element, 'get_slices_div');

    //send data to server
    $('.video_id', element).submit(function(eventObject) {
        var video_id = $('#video_id').val();
        $.ajax({
            type: "POST",
            url: handlerVideoSlices,
            data: JSON.stringify({"video_id": video_id}),
            success: updateSlice
        });
    });


    $(function ($) {
        /* Here's where you'd do things on page load. */
        $.ajax({
            type: "POST",
            url: getVideoSlices,
            data: JSON.stringify({"video_id": video_id}),
            success: updateThumbs
        });
    });
}
