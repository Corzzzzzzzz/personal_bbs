$(function () {
    $('#save-banner-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $('#banner-dialog');
        var name_input = dialog.find('input[name="name"]');
        var image_url_input = dialog.find('input[name="image_url"]');
        var link_url_input = dialog.find('input[name="link_url"]');
        var priority_input = dialog.find('input[name="priority"]');

        var name = name_input.val();
        var image_url = image_url_input.val();
        var link_url = link_url_input.val();
        var priority = priority_input.val();
        var submitType = self.attr('data-type');
        var bannerID = self.attr('data-id');

        var url = '';
        if(submitType == 'update'){
            url = '/cms/update_banner/'
        }else{
            url = '/cms/add_banner/'
        }

        zlajax.post({
            'url': url,
            'data': {
                'name': name,
                'image_url': image_url,
                'link_url': link_url,
                'priority': priority,
                'banner_id': bannerID
            },
            'success': function (data) {
                if(data['code'] == 200){
                    dialog.modal('hide');
                    window.location.reload();
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
    $('.edit-banner-btn').click(function (event) {
        var self = $(this);
        var dialog = $('#banner-dialog');
        dialog.modal('show');

        var name_input = dialog.find('input[name="name"]');
        var image_url_input = dialog.find('input[name="image_url"]');
        var link_url_input = dialog.find('input[name="link_url"]');
        var priority_input = dialog.find('input[name="priority"]');
        var SaveBtn = dialog.find('#save-banner-btn');

        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var image_url = tr.attr('data-image');
        var link_url = tr.attr('data-link');
        var priority = tr.attr('data-priority');

        name_input.val(name);
        image_url_input.val(image_url);
        link_url_input.val(link_url);
        priority_input.val(priority);
        SaveBtn.attr('data-type', 'update');
        SaveBtn.attr('data-id', tr.attr('data-id'));

    });
});

$(function () {
    $('.delete-banner-btn').click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr('data-id');

        xtalert.alertConfirm({
            'msg': '确定删除该轮播图？',
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/del_banner/',
                    'data': {
                        'banner_id': banner_id
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


$(function () {
   zlqiniu.setUp({
       'domain': 'http://phabnmfef.bkt.clouddn.com/',
       'browse_btn': 'upload-banner-btn',
       'uptoken_url': '/common/upload_qiniu/',
       'success': function (up, file, info) {
           var image_input = $('input[name="image_url"]');
           image_input.val(file.name);
       },
   })
});