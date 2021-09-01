var django_ajax_form = {
      var: {
          form_html: '',
          url: '',
      },
      OpenForm: function(url) {
        console.log(url);
        $('.modal-body').height('auto');
	django_ajax_form.var.url = url;

        //  var crispy_form_load = $.get( "/applications/272/vessel/" ).responseText;
        //  alert(crispy_form_load);
        $('#vesselModal').remove();

	$.ajax({
	    url: url,
	    async: false,
	    success: function(data) {
        	  django_ajax_form.var.form_html = data;
	    }
	});

        var csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();

        var htmlvalue = "";
            htmlvalue += '<div id="vesselModal" class="modal fade" role="dialog">';
            htmlvalue += '<div class="modal-dialog modal-lg">';
            htmlvalue += '    <div class="modal-content">';
            htmlvalue += '      <div class="modal-header">';
            htmlvalue += '        <button type="button" class="close" data-dismiss="modal">&times;</button>';
            htmlvalue += '        <h4 class="modal-title"></h4>';
            htmlvalue += '      </div>';
            htmlvalue += '      <div class="modal-body" style="overflow: auto;">';
            htmlvalue += django_ajax_form.var.form_html;
            htmlvalue += '<form action="/applications-uploads/" method="post" enctype="multipart/form-data" id="upload_form">';
            htmlvalue += '<input type="hidden" name="csrfmiddlewaretoken" value="'+csrfmiddlewaretoken+'" />';
            htmlvalue += '</form>';
            htmlvalue += '<BR><BR>';
            htmlvalue += '<BR><BR>';
            htmlvalue += '</div>';
            htmlvalue += '<div class="modal-footer">';
            htmlvalue += '<BR><BR><button name="close" type="button" class="btn btn-primary" value="Close" class="close" data-dismiss="modal" value="Close">Close</button>';
            htmlvalue += '</div>';
            htmlvalue += '</div>';
            htmlvalue += '</div>';
            htmlvalue += '</div>';
            htmlvalue += '</div>';

            $('html').prepend(htmlvalue);
	    $('#vesselModal').modal({
                 show: 'false'
            });
            $( window ).resize(function() {
                             var modalbodyheight = window.innerHeight * 0.7;
                             $('.modal-body').height(modalbodyheight+'px');
            });
            var modalbodyheight = window.innerHeight * 0.7;
            $('.modal-body').height(modalbodyheight+'px');

 // $('#vesselModal').modal('show');
$('#vesselModal').show();

$('#id_form_modals').submit(function(event) {
event.preventDefault();
});


$('.ajax-submit').on("click", function(event) {
    django_ajax_form.saveForm();
});

$('.ajax-close').on("click", function(event) {
    django_ajax_form.CloseForm();
});
$("#vesselModal").on("hidden.bs.modal", function () {
    $('.modal-body').html('');
    $('.modal-body').height('auto');
    // put your default event here
});

    $(function() {
        // Initialise datepicker widgets.
        $(".dateinput").datepicker({
            format: 'dd/mm/yyyy',
            autoclose: true,
            todayHighlight: true
        });
    });


      },
      saveForm: function()  { 


var form_data = new FormData($('#id_form_modals')[0]);
$.ajax({
url : django_ajax_form.var.url,
type: "POST",
data : form_data,
contentType: false,
cache: false,
processData:false,
xhr: function() {
//upload Progress
var xhr = $.ajaxSettings.xhr();
return xhr;
},
mimeType:"multipart/form-data"
}).done(function(res) { //
        django_form_checks.var.form_changed = 'changed';
//        console.log('upload complete');
//        var input_array =[];
$('#vesselModal').modal('hide');
if (res.indexOf('alert-danger') >= 0 ) { 
        console.log("ERROR Found in response");
        var csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();

        var htmlvalue = "";
            htmlvalue += '<div id="vesselModal" class="modal fade" role="dialog">';
            htmlvalue += '<div class="modal-dialog modal-lg">';
            htmlvalue += '    <div class="modal-content">';
            htmlvalue += '      <div class="modal-header">';
            htmlvalue += '        <button type="button" class="close" data-dismiss="modal">&times;</button>';
            htmlvalue += '        <h4 class="modal-title"></h4>';
            htmlvalue += '      </div>';
            htmlvalue += '      <div class="modal-body" style="overflow: auto;">';
            htmlvalue += res;
            htmlvalue += '<form action="/applications-uploads/" method="post" enctype="multipart/form-data" id="upload_form">';
            htmlvalue += '<input type="hidden" name="csrfmiddlewaretoken" value="'+csrfmiddlewaretoken+'" />';
            htmlvalue += '</form>';
            htmlvalue += '<BR><BR>';

            htmlvalue += '<BR><BR>';
            htmlvalue += '<div class="modal-footer">';
            htmlvalue += '<BR><BR><button name="close" type="button" class="btn btn-primary" value="Close" class="close" data-dismiss="modal" value="Close">Close</button>';
            htmlvalue += '</div>';
            htmlvalue += '</div>';
            htmlvalue += '</div>';
            htmlvalue += '</div>';
            htmlvalue += '</div>';

            $('html').prepend(htmlvalue);
            $('#vesselModal').modal({
        show: 'false'
 });

if (typeof loadForm == 'function') { 
  loadForm(); 
} else {
  console.log("no loadForm");
}
$('#id_form_modals').submit(function(event) {
event.preventDefault();
});


$('.ajax-submit').on("click", function(event) {
django_ajax_form.saveForm();

});
$('.ajax-close').on("click", function(event) {
django_ajax_form.CloseForm();

});

    $(function() {
        // Initialise datepicker widgets.
        $(".dateinput").datepicker({
            format: 'dd/mm/yyyy',
            autoclose: true,
            todayHighlight: true
        });
    });


        // $(form_id)[0].reset(); //reset form
        // $(result_output).html(res); //output response from server
//        var obj = JSON.parse(res);
 //       var input_id_obj = $('#'+input_id+'_json').val();

//        if (upload_type == 'multiple') {

 //       if (input_id_obj.length > 0) {
 //       	input_array = JSON.parse(input_id_obj);
 //       }

//        input_array.push(obj);
 //       console.log(obj['doc_id']);
 //       console.log(input_id);

   //     } else {
        //        input_array = obj
  //      }

    //    $('#'+input_id+'_json').val(JSON.stringify(input_array));
    //    submit_btn.val("Upload").prop( "disabled", false); //enable submit button once ajax is done
    //    ajax_loader_django.showFiles(input_id,upload_type);
    //    $('#'+input_id+'__submit__files').val('');
// $('#vesselModal').modal('hide');
// $('#vesselModal').modal('hide');
// $('#vesselModal').hide();
$('#vesselModal').show();
}
if (typeof loadForm == 'function') {
  loadForm();
} else {
  console.log('no loadForm');
}

// $( "#vesselModal" ).remove();
}).fail(function(res) { //
        console.log('failed');

        $(result_output).append('<div class="error">Upload to Server Error</div>');
        $('#progress-bar-indicator').attr('class', 'progress-bar progress-bar-danger');

        var percent = '100';
        $(progress_bar_id +" .progress-bar").css("width", + percent +"%");
        $(progress_bar_id + " .status").text("0%");
        $(progress_bar_id + " .status-text").text("error");
        //submit_btn.val("Upload").prop( "disabled", false);
        });
$('#vesselModal').show();

//	$('#vesselModal').modal({
//                   show: 'true'
  //          });

//	$('#vesselModal').modal('hide');

// $('#vesselModal').hide();

},
CloseForm: function() {
   $('#vesselModal').modal('hide');
}

}


//      }

//}
