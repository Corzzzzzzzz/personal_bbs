
$(function () {
   $('#submit-btn').click(function (event) {
       event.preventDefault();
       var telephone_input = $("input[name='telephone']");
       var password_input = $("input[name='password']");
       var remember_me_input = $("input[name='remember_me']");

       var telephone = telephone_input.val();
       var password = password_input.val();
       var remember_me = remember_me_input.val();

       zlajax.post({
           'url': '/login/',
           'data':{
               'telephone': telephone,
               'password': password,
               'remember_me': remember_me
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