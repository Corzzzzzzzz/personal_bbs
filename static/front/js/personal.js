$(function () {
    $('#follow-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var div = self.parent().parent();
        var followed_id = div.attr('data-id');
        var relation = div.attr('data-relation');
        if(relation){
            xtalert.alertConfirm({
                'title': '取消关注',
                'msg': '确定取消关注',
                'confirmCallback': function () {
                    zlajax.post({
                        'url': '/add_follow_relation/',
                        'data':{
                            'followed_id': followed_id
                        },
                        'success': function (data) {
                            if(data['code']==200){
                                xtalert.alertSuccessToast('取消成功');
                                setTimeout(function () {
                                    window.location.reload()
                               }, 500)
                            }else{
                                xtalert.alertInfo(data['message'])
                            }
                        },
                        'fail': function (error) {
                            xtalert.alertNetworkError()
                        }
                    })
                }
            })
        }else{
            zlajax.post({
                'url': '/add_follow_relation/',
                'data':{
                    'followed_id': followed_id
                },
                'success': function (data) {
                    if(data['code']==200){
                        xtalert.alertSuccessToast('关注成功');
                        setTimeout(function () {
                            window.location.reload()
                       }, 500)
                    }else{
                        xtalert.alertInfo(data['message'])
                    }
                },
                'fail': function (error) {
                    xtalert.alertNetworkError()
                }
            })
        }
    })
});