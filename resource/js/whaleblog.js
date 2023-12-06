function showLogin() {
    $("#loginlabel").addClass("active");
    $("#registerlabel").removeClass("active");
    $("#LoginPanel").modal('show');
}

function showReg() {
    $("#loginpanel").addClass("active");
    $("#registerlabel").removeClass("active");
    $("#RegisterPanel").modal('show');
}

//返回页面顶端
function gotoTop() {
    $('html,body').animate({scrollTop: 0}, 400);
    return false
}

function doLogin(e) {
    if (e != null && e.keyCode != 13) {
        return false
    }
    var logName = $.trim($("#logname").val());
    var logPass = $.trim($("#logpass").val());
    var logCode = $.trim($("#logcode").val());
    if (!logName.match('.+@.+\..+')) {
        bootbox.alert({'title': "错误提示", "message": "用户名格式不正确"});
        return false;
    } else {
        param = "username=" + logName;
        param += "&password=" + logPass;
        param += "&vcode=" + logCode;
        //利用jquery框架发送POST请求，并获取到后台接口的响应数据
        $.post('/login', param, function (data) {
            console.log(data)
            if (data == 'vcode-error') {
                bootbox.alert({'title': "错误提示", "message": "验证码错误"});
                $("#logcode").val('');
                $("#logcode").focus();
            } else if (data == 'log-fail') {
                bootbox.alert({'title': "错误提示", "message": "用户名或密码不正确"});
            } else if (data == 'log-pass') {
                bootbox.alert({'title': "信息提示", "message": "恭喜你,登录成功！"});
                //注册成功后延迟一秒刷新页面
                setTimeout('location.reload();', 1000)
            }
        })
    }
}


function dosendMail(obj) {
    var email = $.trim($("#regname").val());
    //对邮箱地址进行校验
    if (!email.match('.+@.+\..+')) {
        bootbox.alert({'title': "错误提示", 'message': "邮箱地址格式不正确!"});
        $("regname").focus()
        return false
    } else {
        $.post('/ecode', 'email=' + email, function (data) {
            if (data == 'email-invalid') {
                bootbox.alert({'title': "错误提示", "message": "邮箱地址不正确"});
                $("#regname").focus();
                return false
            }
            if (data == "send-pass") {
                bootbox.alert({'title': "信息提示", "message": "邮箱验证码已发送，请尽快填写"});
                $("#regname").attr('disabled', true)
                $(obj).attr('disabled', true)
                return false
            } else {
                bootbox.alert({'title': "信息提示", "message": "邮箱验证码未能成功发送"});
                return false
            }
        })
    }
}

function doReg(e) {
    if (e != null && e.keyCode != 13) {
        return false
    }
    var regName = $.trim($("#regname").val());
    var regPass = $.trim($("#regpass").val());
    var regNick = $.trim($("#regnick").val());
    var regCode = $.trim($("#regcode").val());
    if (!regName.match('.+@.+\..+') || regPass.length < 5) {
        bootbox.alert({'title': "错误提示", "message": "密码长度不得少于5位"});
        return false;
    } else {
        param = "username=" + regName;
        param += "&nickname=" + regNick;
        param += "&password=" + regPass;
        param += "&ecode=" + regCode;
        //利用jquery框架发送POST请求，并获取到后台接口的响应数据
        $.post('/user', param, function (data) {
            if (data == 'ecode-error') {
                bootbox.alert({'title': "错误提示", "message": "验证码错误"});
                $("#regcode").val('');
                $("#regcode").focus();
            } else if (data == 'user-repeated') {
                bootbox.alert({'title': "错误提示", "message": "用户名已被注册"});
            } else if (data == 'up-invalid') {
                bootbox.alert({'title': "错误提示", "message": "邮箱地址不正确或少于5位"});
            } else if (data == 'reg-pass') {
                bootbox.alert({'title': "信息提示", "message": "恭喜你,注册成功！"});
                //注册成功后延迟一秒刷新页面
                setTimeout('location.reload();', 1000)
            } else if (data == "reg-fail") {
                bootbox.alert({'title': "错误提示", "message": "注册失败"});
            }
        })
    }
}