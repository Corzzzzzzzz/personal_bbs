

$(function () {
    $("#submit").click(function (event) {
        //up:获取上传按钮的点击时间
        //down：阻止按钮默认的提交表单事件
        event.preventDefault();

        var oldpwdE = $("input[name=old_password]");
        var newpwdE = $("input[name=new_password]");
        var newpwd2E = $("input[name=new_password_repeat]");

        var old_password = oldpwdE.val();
        var new_password = newpwdE.val();
        var new_password_repeat = newpwd2E.val();


        //在模板的meta中渲染csrf_token   --name及content
        //在ajax的头部中设置X-CSRFtoken    --zlajax.js中已封装
        zlajax.post({
            'url':'/cms/resetpwd/',
            'data':{
                'old_password': old_password,
                'new_password': new_password,
                'new_password_repeat': new_password_repeat
            },
            'success': function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('恭喜！秘密修改成功');
                    oldpwdE.val('');
                    newpwdE.val('');
                    newpwd2E.val('');
                }else{
                    var message = data['message'];
                    xtalert.alertInfo(message);
                }
            },
            'fail': function (error) {
                xtalert.alertNetworkError();
            }

        });


    });
});