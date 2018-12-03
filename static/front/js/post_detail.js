
$(function () {
   ue = UE.getEditor("editor", {
       'serverUrl': 'ueditor/upload/',
       'toolbars': [
            [
                'undo', //撤销
                'redo', //重做
                'bold', //加粗
                'italic', //斜体
                'source', //源代码
                'blockquote', //引用
                'selectall', //全选
                'insertcode', //代码语言
                'fontfamily', //字体
                'fontsize', //字号
                'simpleupload', //单图上传
                'emotion' //表情
            ]
        ]
   });
   window.ue = ue;
});

$(function () {
    $('#comment-submit-btn').click(function (event) {
        event.preventDefault();
        var loginTag = $('#login-tag').attr('data-login');

        if(!loginTag){
            window.location = '/login/';
        }else{
            var content = window.ue.getContent();
            var post_id = $('#post-content').attr('data-id');

            zlajax.post({
                'url': '/add_comment/',
                'data': {
                    'content': content,
                    'post_id': post_id
                },
                'success': function (data) {
                    if(data['code']==200){
                        window.location.reload();
                    }else{
                        xtalert.alertInfo(data['message'])
                    }
                },
                'fail': function (error) {
                    xtalert.alertNetworkError()
                }
            });
        }
    });
});

$(function () {
   $('#like-post-btn').click(function (event) {
       event.preventDefault();
       var self = $(this);
       var loginTag = $('#login-tag').attr('data-login');

       if(!loginTag){
            window.location = '/login/';
       }else{
           var post_id = self.parent().parent().attr('data-id');
           zlajax.post({
               'url': '/like/',
               'data': {
                   'post_id': post_id
               },
               'success': function (data) {
                   if(data['code']==200){
                       xtalert.alertSuccessToast('操作成功');
                        setTimeout(function () {
                            window.location.reload()
                       }, 500);
                   }else{
                       xtalert.alertInfo(data['message'])
                   }
               },
               'fail': function (error) {
                    xtalert.alertNetworkError();
               }
           });
       }
   });
});

$(function () {
   $('.handle-comment-btn').click(function (event) {
       event.preventDefault();
       var self = $(this);
       var comment_id = self.attr('data-commentID');
       var type = self.attr('data-type');
       var url = '';
       var msg = '';
       if(type == 'delete'){
           url = '/delete_comment/',
           msg = '我要删除！'
       }else{
           url = '/inform_comment/',
           msg = '我要举报!'
       }
       xtalert.alertConfirm({
           'msg': '再确认一下吧',
           'confirmText': msg,
           'cancelText': '算了算了',
           'confirmCallback': function () {
               zlajax.post({
                   'url': url,
                   'data':{
                       'comment_id': comment_id
                   },
                   'success': function (data) {
                       if(data['code']==200){
                           xtalert.alertSuccessToast('操作成功');
                            setTimeout(function () {
                                window.location.reload()
                           }, 500);
                       }else{
                           xtalert.alertInfo(data['message'])
                       }
                   },
                   'fail': function (error) {
                       xtalert.alertNetworkError()
                   }
               })
           },
       })
   })
});