jQuery(function ($){
    jQuery.noConflict();

    $(document).ready(function() {

// Gets the video src from the data-src on each button

var $videoSrc;

$('.video-btn').click(function() {
    $videoSrc = '';
    $videoSrc = $(this).data( "src" ).replace('watch?v=','embed/');
});

$('.indicaciones-btn').click(function() {
    $indicaciones = $(this).data( "src" );
    $(".indicaciones-txt").html($indicaciones);
});

// when the modal is opened autoplay it
$('#modalvideo').on('shown.bs.modal', function (e) {
    // set the video src to autoplay and not to show related video. Youtube related video is like a box of chocolates... you never know what you're gonna get
    $("#video").attr('src',$videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0" );
})
  

$('#modalvideo').on('hide.bs.modal', function (e) {
    $("#video").attr('src','');
})

$('.video-insta').click(function() {
    $(".videoinsta-txt").html($(this).data( "src" ));
});



$('#submitenviar').on("click", function(event){
    event.preventDefault();
    url = window.location.href;
    data_serialize = $("#formmedidas").serialize();
    $.ajax({
                url: url,
                type: 'POST',
                data: data_serialize,
                success: function(response){
                    if(response){
                        window.location.href = url;
                    }
                },

     });
});

});

});

