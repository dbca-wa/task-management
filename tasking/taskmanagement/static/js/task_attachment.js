var task_attachment = {
    var: {
        attachment_cache: [],
	reader: null
    },
    upload: function() {
           
    },
    handleFileSelect: function(evt) {
        var files = evt.target.files;
	console.log("FILE LENGTH");
	console.log(files.length);
        console.log(files);
        for (var i = 0; i < files.length; i++) {
	     console.log("PPP");
             console.log(i);
             // text += cars[i] + "<br>";
	    
             var file = files[i];
             if (files && file) {
                  var reader = new FileReader();
                  reader['filename'] = file.name; 
		  reader.readAsDataURL(file);
		  task_attachment.var.reader = reader;
		  task_attachment.var.attachment_cache.push({'filename': reader.filename, 'reader': reader});
		  task_attachment.refresh_attachment_preview();
		  //console.log(reader.readAsBinaryString(file));

             }
        }
	
    }, 
    refresh_attachment_preview: function() {
	console.log("REFESH LIST");    
        var html = '';
        for (var i = 0; i < task_attachment.var.attachment_cache.length; i++) {
	      var filenamelength = task_attachment.var.attachment_cache[i].filename.length;
	      var shortfilename = "";
              if (filenamelength > 10) {
                   shortfilename = ".."+task_attachment.var.attachment_cache[i].filename.substring(filenamelength-10,filenamelength);
              } else {
                   shortfilename = task_attachment.var.attachment_cache[i].filename;
              }
              html += "<div class='text-center' style='padding: 10px; height: 130px; width: 120px; display: inline-block; margin-right: 5px;'>";
	      html += "<div class='text-center'><img src='/static/images/file-extenion-icons/48px/"+task_attachment.file_extension(task_attachment.var.attachment_cache[i].filename).toLowerCase()+".png'></div>";
	      html += "<div>"+shortfilename+"</div>";
	      html += "<div><button class='btn btn-danger btn-sm' onclick='task_attachment.delete_attachment("+i+");'>DELETE</button></div>";
	      html += "</div>";
              console.log(task_attachment.var.attachment_cache[i].filename);
        }


        $('#attached_files').html(html);



    },
    file_extension: function(filename) {
          var extension = '_blank';
	  var fnamelength = filename.length;
	  var threeextstart = fnamelength - 4;
	  var threeextend = fnamelength - 3;
          if (filename.substring(threeextstart,threeextend) == '.') {
	       extension = filename.substring(threeextstart+1,fnamelength);
          }
          if (filename.substring(threeextstart-1,threeextend-1) == '.') {
	       extension = filename.substring(threeextstart-1+1,fnamelength);
	  }
          return extension;

	  // if (file_extension == 
    },
    delete_attachment: function(index) {
         task_attachment.var.attachment_cache.splice(index, 1);
	 task_attachment.refresh_attachment_preview();
    }	    

}    

