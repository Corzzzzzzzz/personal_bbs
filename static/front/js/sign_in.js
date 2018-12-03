
$(function () {
    $('#captcha-img').click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = zlparam.setParam(src, 'xx', Math.random());
        self.attr('src', newsrc);
    });
});

$(function () {
    $('#sms_captcha').click(function(event){
        event.preventDefault();
        var self = $(this);
        var telephone = $('input[name="telephone"]').val();
        if(!telephone){
            xtalert.alertInfoToast('请输入手机号');
            return;
        }
        var timestamp = (new Date).getTime();
        var sign = md5(telephone+timestamp+'as43&%HUGgygTFYVcdse2');
        zlajax.post({
            'url': '/common/sms_captcha/',
            'data': {
                'telephone': telephone,
                'timestamp': timestamp,
                'sign' : sign
            },
            'success': function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('短信验证码发送成功！请注意查收！');
                    self.attr('disabled','disabled');
                    var timeCount = 60;
                    var timer = setInterval(function () {
                        timeCount--;
                        self.text(timeCount);
                        if(timeCount <= 0){
                            self.removeAttr('disabled');
                            clearInterval(timer);
                            self.text('获取验证码');
                        }
                    }, 1000);
                }else{
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                xtalert.alertNetworkError();
            }
        });
    });
});

$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var telephone_input = $("input[name='telephone']");
        var sms_captcha_input = $("input[name='sms_captcha']");
        var username_input = $("input[name='username']");
        var password1_input = $("input[name='password1']");
        var password2_input = $("input[name='password2']");
        var graph_captcha_input = $("input[name='graph_captcha']");

        var telephone = telephone_input.val();
        var sms_captcha = sms_captcha_input.val();
        var username = username_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();
        var graph_captcha = graph_captcha_input.val();

        zlajax.post({
            'url': '/sign_in/',
            'data': {
                'telephone': telephone,
                'sms_captcha': sms_captcha,
                'username': username,
                'password1': password1,
                'password2': password2,
                'graph_captcha': graph_captcha
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var return_to = $('#return-to-span').text();
                    if(return_to){
                        window.location = return_to;
                    }else {
                        window.location = '/';
                    }
                }else{
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                xtalert.alertNetworkError();
            }
        });
    });
});