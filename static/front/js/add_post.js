$(function () {
   var ue = UE.getEditor('editor', {
       "serverUrl": '/ueditor/upload/'
   });

   $('#submit-btn').click(function (event) {
       event.preventDefault();
       var title_input = $('input[name="title"]');
       var board_id_input = $('select[name="board_id"]');

       var title = title_input.val();
       var board_id = board_id_input.val();
       var content = ue.getContent();

       zlajax.post({
           'url': '/add_post/',
           'data': {
               'title': title,
               'board_id': board_id,
               'content': content
           },
           'success': function (data) {
               if(data['code'] == 200){
                   xtalert.alertConfirm({
                       'title': '恭喜！帖子发表成功',
                       'confirmText': '再来一发',
                       'cancelText': '回到首页',
                       'confirmCallback': function () {
                           title_input.val('');
                           ue.setContent('')
                       },
                       'cancelCallback': function () {
                           window.location = '/'
                       }
                   });
               }else{
                   xtalert.alertInfo(data['message']);
               }
           }
       });
   });
});