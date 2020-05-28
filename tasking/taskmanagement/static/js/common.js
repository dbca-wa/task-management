$(function() {
    $('.collapse').on('shown.bs.collapse', function() {
         $(this).parent().find(".glyphicon-chevron-left").removeClass("glyphicon-chevron-left").addClass("glyphicon-chevron-down");

    }).on('hidden.bs.collapse', function() {
	$(this).parent().find(".glyphicon-chevron-down").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-left");
    });

//    $('#vesselModal').bind("DOMSubtreeModified",function() {
	 // alert('changed');

//       $('#id_predefined_conditions').on('click', function() {
//          alert('fff');
//       });
//    });
});
function select_condition(input_id) {

     var input_value = $('#'+input_id).val();
     
     $.ajax({url: "/condition-predefined/"+input_value+"/", contentType: "application/json", dataType: "json", success: function(result) {
         $('#id_condition').val(result['0']['fields']['condition']);
     }});

     $('#'+input_id).val('');


}

function close_popup() {
   $('#overtop').hide();

}

var common = {
     linkify: function(what) {
         str = what; out = ""; url = ""; i = 0;
         do {
             url = str.match(/((https?:\/\/)?([a-z\-]+\.)*[\-\w]+(\.[a-z]{2,4})+(\/[\w\_\-\?\=\&\.]*)*(?![a-z]))/i);
             if(url!=null) {
                 // get href value
                 href = url[0];
                 if(href.substr(0,7)!="http://") href = "http://"+href;
     
                 // where the match occured
                 where = str.indexOf(url[0]);
     
                 // add it to the output
                 out += str.substr(0,where);
     
                 // link it
                 out += '<a href="'+href+'" target="_blank">'+url[0]+'</a>';
     
                 // prepare str for next round
                 str = str.substr((where+url[0].length));
             } else {
                 out += str;
                 str = "";
             }
         } while(str.length>0);
         return out;
     },
     linkify_https: function(what) {
         str = what; out = ""; url = ""; i = 0;
         do {
             url = str.match(/((https?:\/\/)?([a-z\-]+\.)*[\-\w]+(\.[a-z]{2,4})+(\/[\w\_\-\?\=\&\.]*)*(?![a-z]))/i);
             if(url!=null) {
                 // get href value
                 href = url[0];
                 if(href.substr(0,7)!="https://") href = "https://"+href;

                 // where the match occured
                 where = str.indexOf(url[0]);

                 // add it to the output
                 out += str.substr(0,where);

                 // link it
                 out += '<a href="'+href+'" target="_blank">'+url[0]+'</a>';

                 // prepare str for next round
                 str = str.substr((where+url[0].length));
             } else {
                 out += str;
                 str = "";
             }
         } while(str.length>0);
         return out;
     },
     div_text_to_linkify: function(div_id) {
         var div_text = $('#'+div_id).html();
	 div_text = common.linkify(div_text);
	 //div_text = common.linkify_https(div_text);
         $('#'+div_id).html(div_text);

     }






}
