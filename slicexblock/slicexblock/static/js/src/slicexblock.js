/* Javascript for SliceXBlock. */
function SliceXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    function updateSlice(result) {
        $('.slices', element).text(result.video_id);
    }

    var handlerUrl = runtime.handlerUrl(element, 'increment_count');
    var handlerVideoSlices = runtime.handlerUrl(element, 'generate_slices');
    // $('p', element).click(function(eventObject) {
    //     $.ajax({
    //         type: "POST",
    //         url: handlerUrl,
    //         data: JSON.stringify({"hello": "world"}),
    //         success: updateCount
    //     });
    // });

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
    });
}
