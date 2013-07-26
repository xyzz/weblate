$.fn.selectRange = function(start, end) {
    if(!end) end = start;
    return this.each(function() {
        if (this.setSelectionRange) {
            this.focus();
            this.setSelectionRange(start, end);
        } else if (this.createTextRange) {
            var range = this.createTextRange();
            range.collapse(true);
            range.moveEnd('character', end);
            range.moveStart('character', start);
            range.select();
        }
    });
};

function current_textarea(textarea, scroll) {
    textarea.selectRange(textarea.val().length);
    if (scroll) {
        $('html,body').animate({
            scrollTop: textarea.offset().top - ( $(window).height() - textarea.outerHeight(true) ) / 2
        }, 75);
    }
    $(".current_translation").removeClass("current_translation");
    textarea.parents("tr").addClass("current_translation");
}

function next_textarea(current, which) {
    var next;
    if (which == "next")
        next = current.parents("tr").next();
    else if (which == "prev")
        next = current.parents("tr").prev();
    if (!next.length)
        return;
    current_textarea(next.find("textarea"), true);
}

function submit_textarea(textarea) {
    var elem = $(textarea);
    $.post("../translate/", {
        csrfmiddlewaretoken: $.cookie("csrftoken"),
        checksum: elem.data("checksum"),
        target: elem.val()
    })
        .done(function(){elem.addClass("completed");})
        .fail(function(){elem.addClass("fail")})
        .always(function(){elem.removeClass("loading modified");});
    elem.removeClass("completed fail");
    elem.addClass("loading");
}

var zen_initial = {};

function init_zen() {
    var textareas = $(".zen textarea.target");
    textareas.each(function(){
        zen_initial[$(this).data("checksum")] = this.value;
    }).bind('input propertychange', function() {
        if ($(this).val() != zen_initial[$(this).data("checksum")])
            $(this).addClass("modified");
        else
            $(this).removeClass("modified");
    });
    current_textarea(textareas.first());
    $(document).on("keydown", "textarea.target", function (e) {
        if (!e.ctrlKey)
            return;
        if (e.keyCode == 13 || e.keyCode == 10) {
            submit_textarea(this);
            next_textarea($(this), "next");
        }
        if (e.keyCode == 40)
            next_textarea($(this), "next");
        if (e.keyCode == 38)
            next_textarea($(this), "prev");
    });
    $(document).on("focus", "textarea.target", function() {
        current_textarea($(this));
    });
}

$(function(){init_zen();});
