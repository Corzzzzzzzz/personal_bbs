$(function () {
   $('#account-save-btn').click(function (event) {
       event.preventDefault();
       var usernameIput = $('input[name="username"]');
       var emailInput = $('input[name="email"]');
       var realnameInput = $('input[name="realname"]');
       var signatureInput = $('textarea[name="signature"]');
       var genderInput = $('input[name="genderOption"]');
       var image_img = $('#avatar-img');

       var username = usernameIput.val();
       var email = emailInput.val();
       var realname = realnameInput.val();
       var signature = signatureInput.val();
       var gender = genderInput.val();
       var avatar_url = image_img.attr('src');

       zlajax.post({
           'url': '/account/',
           'data': {
               'username': username,
               'email': email,
               'realname': realname,
               'signature': signature,
               'gender': gender,
               'avatar_url': avatar_url
           },
           'success': function (data) {
               if(data['code']==200){
                   xtalert.alertSuccessToast();
                   setTimeout(function () {
                        window.location = '/account/'
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


$(function () {
   zlqiniu.setUp({
       'domain': 'http://phabnmfef.bkt.clouddn.com/',
       'browse_btn': 'upload-avatar-btn',
       'uptoken_url': '/common/upload_qiniu/',
       'success': function (up, file, info) {
           var image_img = $('#avatar-img');
           image_img.attr('src', file.name)
       },
   });
});
