var task = {
	var: {
		'test': 'test',
                'no_comment_allow': false,
                'current_action': ''
	},
        no_comment_confirm: function() { 
            task.var.no_comment_allow = true;
            if (task.var.current_action == 'close') { 
               task.close_task();
            } else {
		task.defer_task();
 	    }
        },
        defer_task: function() {
            task.var.current_action == 'defer';
            if (task.var.no_comment_allow == false) {
		if (task.no_comment_check() == true) {
	            task.submit_task_entry('defer');
		}
            } else {
                task.submit_task_entry('defer');
            }
 	},
	close_task: function() {
            task.var.current_action == 'close';
            if (task.var.no_comment_allow == false) { 
                  if (task.no_comment_check() == true) { 
			task.submit_task_entry('close');	  
	          } 
            } else {
                  task.submit_task_entry('close');
            }
	},
	no_comment_check: function() {
            var task_comment = $('#task_comment').val();
            if (task_comment.length < 1) {
                $('#NoCommentModal').modal('show');
                return false;
            }
            return true;
 	},
 	submit_task_entry: function(status) {
            var task_id = $('#task_id').val();
            var task_comment = $('#task_comment').val();
	    var task_deferred_date = $('#task_deferred_date').val();
             
            //if (task.var.no_comment_allow == false) {
	    //    console.log(task_comment.length)
            //    if (task_comment.length < 1) {
            //        $('#NoCommentModal').modal('show');
	    //        return false;
	    //    }
            //}
            var ta = [];
            for (var i = 0; i < task_attachment.var.attachment_cache.length; i++) {
	            var filename = task_attachment.var.attachment_cache[i].filename;
		    var base64file = task_attachment.var.attachment_cache[i].reader.result;
		    ta.push({'filename': filename, 'base64file': base64file })

            }
		
            var form_data =  { 'task_id': task_id,
		               'task_status': status,
		               'task_comment': task_comment,
	                       'task_deferred_date' : task_deferred_date,
		               'task_attachments' : JSON.stringify(ta) 
	                     };

            console.log(form_data);

            $.ajax({
               type: "post",
               url: "/api/create_task_comment/",
               data:form_data,
               error: function(result) {
                      task_response_notification.error('');
               },
               success: function (result) {
		       task_response_notification.success('Please wait reloading task');
                       setTimeout(function(){ window.location = "/view-task/"+task_id+"/"; }, 1000);
		       console.log(result);
               }
           })


            // Reset Vars
            task.var.no_comment_allow = false;
            task.var.current_action = '';
	}


}
