$(function () {
    $('#captcha-img').click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = zlparam.setParam(src, 'xx', Math.random());
        self.attr('src', newsrc);
    });
});

$(function () {
    $('#sms_captcha').click(function (event) {
        event.preventDefault();
        var self = $(this);

        var telephone = $('input[name="telephone"]').val();
        var timestamp = (new Date).getTime();
        var sign = md5(telephone+timestamp+'as43&%HUGgygTFYVcdse2');

        zlajax.post({
            'url': '/common/sms_captcha/',
            'data': {
                'telephone': telephone,
                'timestamp': timestamp,
                'sign': sign
            },
            'success': function (data) {
                if(data['code']==200){
                    xtalert.alertSuccessToast('验证码发送成功，请查收');
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
                    xtalert.alertInfo(data['message'])
                }
            },
            'fail': function (error) {
                xtalert.alertNetworkError()
            }
        })
    })
});


$(function () {
   $('#account-save-btn').click(function (event) {
       event.preventDefault();

       var telephoneInput = $('input[name="telephone"]');
       var sms_captchaInput = $('input[name="sms-captcha"]');
       var old_passwordInput = $('input[name="old-password"]');
       var password1Input = $('input[name="password1"]');
       var password2Input = $('input[name="password2"]');
       var graph_captchaInput = $('input[name="graph-captcha"]');

       var telephone = telephoneInput.val();
       var sms_captcha = sms_captchaInput.val();
       var old_password = old_passwordInput.val();
       var password1 = password1Input.val();
       var password2 = password2Input.val();
       var graph_captcha = graph_captchaInput.val();

       zlajax.post({
           'url': '/security/',
           'data': {
               'telephone': telephone,
               'sms_captcha': sms_captcha,
               'old_password': old_password,
               'password1': password1,
               'password2': password2,
               'graph_captcha': graph_captcha
           },
           'success': function (data) {
               if(data['code']==200){
                   xtalert.alertSuccessToast('恭喜，密码修改成功');
                   setTimeout(function () {
                        window.location = '/security/'
                   }, 500)
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


