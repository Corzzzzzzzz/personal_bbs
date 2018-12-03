$(function () {
   $('.highlight-btn').click(function (event) {
       event.preventDefault();
       var self = $(this);
       var tr = self.parent().parent();
       var post_id = tr.attr('data-id');
       var high_light  = parseInt(tr.attr('data-highlight'));

       var url = '';
       if(high_light){
           url = '/cms/unhl_post/'
       }else{
           url = '/cms/hl_post/'
       }

       zlajax.post({
           'url': url,
           'data': {
               'post_id':post_id
           },
           'success': function (data) {
               if(data['code']==200){
                   xtalert.alertSuccessToast('操作成功');
                   setTimeout(function () {
                        window.location = '/cms/posts/'
                   }, 500)
               }else{
                    xtalert.alertInfo(data['message'])
               }
           },
           'fail': function (error) {
               xtalert.alertNetworkError()
           }
       });
   });
});