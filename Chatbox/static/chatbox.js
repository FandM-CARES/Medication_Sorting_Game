function message(botm) {
    // if there's user input
    // if ($('#user').val()) {
    //     addUserInput();
    // }

    addUserInput(botm);

    // create a row div
    var botRow = document.createElement("div");
    $(botRow).addClass("row");

    // create a newbotDiv div
    var newBotDiv = document.createElement("div");
    $(newBotDiv).addClass("newbotDiv");

    // set text to bot output
    $(newBotDiv).append(botm["start"]);
    if (botm['state']){
      $(newBotDiv).append(botm["state"] + "\n");
    }
    $(newBotDiv).append(botm["hint"]);
    $(newBotDiv).append(botm["end"]);

    // add newbotDiv as child of row and add row to child of chatSpace
    $(botRow).append($(newBotDiv));
    $("#chatSpace").append($(botRow));

    // TODO add debugging log
    // TODO add avatar status
}

function addUserInput(botm) {
    // create a row div
    var userRow = document.createElement("div");
    $(userRow).addClass("row");

    // create a newuserDiv div and set text to user input
    var newUserDiv = document.createElement("div");
    console.log(botm["start"])
    $(newUserDiv).addClass("newuserDiv")
                 .html($('#user').val())
    // add newuserDiv as child of row, and add row as child of chatSpace
    $(userRow).append($(newUserDiv));
    $("#chatSpace").append($(userRow));
}

function updateScroll() {
    $("#chatSpace").scrollTop($("#chatSpace")[0].scrollHeight);
}

$(document).ready(function () {

    $.post($SCRIPT_ROOT + "/startgame", {    },
        function (data) {
          message(data);
          updateScroll();
    });

    

    // TODO break this down like a controller function
    

    

    // TODO move this to an init file
    animateAvatar("sleeping");

    // TODO also put this in an init file
    $("#btnSleeping").click(function() {animateAvatar('sleeping')});
    $("#btnThinking").click(function() {animateAvatar('thinking')});
    $("#btnListening").click(function() {animateAvatar('listening')});
    $("#btnSpeaking").click(function() {animateAvatar('speaking')});

    // TODO also put this in an init file
    $(".toggleDebug").click(function() {
        $("#debug").toggle("slow", function(){});
        $(".toggleDebug").toggleClass("debugOn");
    });

    // this used to be a <form>
    $("#submitBtn").on('click', function (event) {
        $.post($SCRIPT_ROOT + "/message", {
            botm: $('#user').val()
        }, function (data) {
            message(data);
            updateScroll();
        });
        // if using <form>, this has something to do with not refreshing
        return false;
        // Joseph's code. Maybe this is the same as the above return false?
        // 	event.preventDefault();
    });
});