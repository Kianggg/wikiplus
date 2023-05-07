$( document ).ready(function() {
    $("#content-tab").on( "click", function() { show_content() } );
    $("#gallery-tab").on( "click", function() { show_gallery() } );

    show_content();
})

// Show the content view and hide everything else
function show_content() {
    $("#content-view").show();
    $("#gallery-view").hide();
}

// Show the gallery view and hide everything else
function show_gallery() {
    $("#content-view").hide();
    $("#gallery-view").show();
}