$(document).ready(function () {

    var animating = false,
        submitPhase1 = 1100,
        submitPhase2 = 400,
        $login = $(".login");

    function ripple(elem, e) {
        $(".ripple").remove();
        var elTop = elem.offset().top,
            elLeft = elem.offset().left,
            x = e.pageX - elLeft,
            y = e.pageY - elTop;
        var $ripple = $("<div class='ripple'></div>");
        $ripple.css({top: y, left: x});
        elem.append($ripple);
    }

    $(document).on("click", ".login__submit", function (e) {
        if (animating) return;
        animating = true;
        var that = this;
        var user = {};
        user.username = $('#username').val();
        user.passwd = $('#passwd').val();
        ripple($(that), e);
        $(that).addClass("processing");
        setTimeout(function () {
            $(that).addClass("success");
            setTimeout(function () {
                $login.hide();
                $login.addClass("inactive");
                animating = false;
                $(that).removeClass("success processing");
            }, submitPhase2);
            $.post('/login_validation', user, function (data) {
                if (data['result']) {
                    window.location.href = 'part';
                } else {
                    alert('账号或密码错误');
                    window.location.href = '';
                }
            })
        }, submitPhase1);
    });

});