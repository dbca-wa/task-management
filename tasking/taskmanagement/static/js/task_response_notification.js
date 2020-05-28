var task_response_notification = {
	var: {},
	success: function(message) {
              $('#task_response_popup').remove();
	      var html = "";
		  var success_message='';
                  if (message.length > 1) { 
	              success_message="<h6>"+message+"<h6>";
	          }
	          html += '<div class="modal fade" id="task_response_popup" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">';
		  html += '  <div class="modal-dialog " role="document" style="width: 350px;">';
		  html += '    <div class="modal-content">';
                  html += '      <div class="modal-body">';
                  html += '        <center><img src="/static/images/success_tick.png" style="width: 290px;"><br><br><h2>SUCCESS</h2>'+success_message+'</center>';
                  html += '      </div>';
                  html += '    </div>';
                  html += '  </div>';
                  html += '</div>';

              console.log(html);
	      $('html').append(html);
              $('#task_response_popup').modal('show');
        },
	warning: function(message) {

	},
	error: function(message) {
	      $('#task_response_popup').remove();
              var html = "";
                var error_message='';
                if (message.length > 1) {
                     error_message="<h6>"+message+"<h6>";
                }
                html += '<div class="modal fade" id="task_response_popup" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">';
                html += '  <div class="modal-dialog " role="document" style="width: 350px;">';
                html += '    <div class="modal-content">';
                html += '      <div class="modal-body">';
                html += '        <center><img src="/static/images/error_critical.png" style="width: 290px;"><br><br><h2>ERROR</h2>'+error_message+'<input type="button" value="Close" class="btn btn-danger" class="close" data-dismiss="modal" aria-label="Close"></center>';
                html += '      </div>';
                html += '    </div>';
                html += '  </div>';
                html += '</div>';

            console.log(html);
            $('html').append(html);
            $('#task_response_popup').modal('show');

	},
	info: function(message) {

	},
	close_popup: function() {
		$('#task_response_popup').modal('hide');
	}




}
