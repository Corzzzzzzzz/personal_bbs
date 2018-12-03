$(function () {
   $('#add-board-btn').click(function (event) {
       event.preventDefault();
       var dialog = $('#board-dialog');
       dialog.modal('show');
   });
});


$(function () {
   $('#save-banner-btn').click(function (event) {
       event.preventDefault();
       var self = $(this);
       var dialog = $('#board-dialog');

       var name_input = dialog.find('input[name="name"]');
       var name = name_input.val();

       var board_id = self.attr('data-id');
       var url ='';
       if(board_id){
           url = '/cms/update_board/'
       }else {
           url = '/cms/add_board/'
       }

       zlajax.post({
           'url': url,
           'data': {
               'name': name,
               'board_id': board_id
           },
           'success': function (data) {
               if(data['code']==200){
                   window.location.reload()
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


$(function () {
    $('.edit-banner-btn').click(function (event) {
        event.preventDefault();
        var dialog = $('#board-dialog');
        dialog.modal('show');

        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var id = tr.attr('data-id');

        var name_input = $('input[name="name"]');
        name_input.val(name);

        var saveBtn = dialog.find('#save-banner-btn');
        saveBtn.attr('data-id', id);
    })
});


$(function () {
    $('.delete-banner-btn').click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var board_id = tr.attr('data-id');

        xtalert.alertConfirm({
            'msg': '确定删除该板块？',
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/del_board/',
                    'data': {
                        'board_id': board_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload()
                        }else {
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

// 点击modal的xx时可以刷新界面
$(function () {
    $('#modal-close-btn').click(function (event) {
        window.location.reload();
    })
});