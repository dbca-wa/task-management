/**
 * @Mulitselect which searchs via ajax and store values in json.
 * @author Jason Moore <jason.mooore@dbca.wa.gov.au>
 *
 * Version        : 1.0.1
 * Created        : 2020-02-29 12:00:00
 */

var mulitselectjm =  {
        var: {searchdata: {}},
        init: function(textarea_id) {
              
              $('#'+textarea_id).before('<div id="div-multiselectjm-'+textarea_id+'" onclick="mulitselectjm.keywordFocus('+"'"+textarea_id+"'"+');"></div>');
              mulitselectjm.init2(textarea_id);

        },
        init2: function(textarea_id) {
             $('#div-multiselectjm-'+textarea_id).html('<div class="select-multiselectjm"><span id="chosen-multiselectjm-'+textarea_id+'"></span><input type="text" class="search-multiselectjm-selection" id="keyword-multiselectjm-'+textarea_id+'" autocomplete="off" onkeyup="mulitselectjm.search(this.value,'+"'"+textarea_id+"'"+');"></div><div id="dropdown-multiselectjm-holder-'+textarea_id+'" style="position:relative; paddding-left:10px; z-index: 30; width: 100%; display:none;"><div id="dropdown-multiselectjm-'+textarea_id+'" style="position:absolute; height: 280px; background-color: #FFFFFF; border: 1px solid #e8e8e8; margin-left: 1px; margin-top: -1px;padding-left: 2px; margin-right: -1px; overflow-y: scroll;">saasas</div></div></div>');
             var width = $('#div-multiselectjm-'+textarea_id).width();
             $('#dropdown-multiselectjm-'+textarea_id).css("width", width+"px");
             var itemdata = $('#'+textarea_id).val();
             if (itemdata == '') {
                 itemdata = "[]";
             }
             var json_data = JSON.parse(itemdata);
             for (i = 0; i < json_data.length; i++) {
                 icon = "";
                 if (typeof  json_data[i]['icon'] != 'undefined') {
                      icon = json_data[i]['icon'];
                 }
                 $('#chosen-multiselectjm-'+textarea_id).before('<span class="select-multiselectjm-selection" style="min-width: 100px;"><img src="'+icon+'" style="margin-top: -4px;">&nbsp;'+json_data[i]['title1']+'<b style="cursor: pointer;" onclick="mulitselectjm.deleteItem('+i+','+"'"+textarea_id+"'"+');">&nbsp;&nbsp;X</b></span>');
             }

        },

        keywordFocus: function(textarea_id) {
                 $('#keyword-multiselectjm-'+textarea_id).focus();
        },
        selectItem: function(item,textarea_id) {
             // mulitselectjm.init2(textarea_id);
             // console.log(mulitselectjm.var.searchdata[item]['title1']);
             var itemdata = $('#'+textarea_id).val();
             if (itemdata == '') {
                 itemdata = "[]";
             }
             var json_data = JSON.parse(itemdata);
             console.log(json_data);
             var item_exists = false;
             for (i = 0; i < json_data.length; i++) {
                 if (mulitselectjm.var.searchdata[item]['id'] ==  json_data[i]['id']) {
                   item_exists = true;
                 }
             }
             if (item_exists == false) { 
                json_data.push(mulitselectjm.var.searchdata[item]);
                $('#'+textarea_id).val(JSON.stringify(json_data));
             }
             // $('#chosen-multiselectjm').before('<span class="select-multiselectjm-selection" style="min-width: 100px;">'+mulitselectjm.var.searchdata[item]['title1']+'<b style="cursor: pointer;" >&nbsp;&nbsp;X</b></span>');
          

             $('#dropdown-multiselectjm-holder-'+textarea_id).slideUp('slow');
             $('#keyword-multiselectjm-'+textarea_id).val("");
             mulitselectjm.init2(textarea_id);
//             for (i = 0; i < json_data.length; i++) {
//                 $('#chosen-multiselectjm').before('<span class="select-multiselectjm-selection" style="min-width: 100px;">'+json_data[i]['title1']+'<b style="cursor: pointer;" >&nbsp;&nbsp;X</b></span>');
//             }
 
        },
        deleteItem: function(item_id, textarea_id) {
             var itemdata = $('#'+textarea_id).val();
             if (itemdata == '') {
                 itemdata = "[]";
             }
             json_data = JSON.parse(itemdata);
             json_data.splice(item_id, 1);
             $('#'+textarea_id).val(JSON.stringify(json_data));
             mulitselectjm.init2(textarea_id);
 
        },
        search: function(keyword, textarea_id) {
                console.log('Key:'+keyword);
                if (keyword.length < 1) {
                      $('#dropdown-multiselectjm-holder-'+textarea_id).slideUp('slow');
                } else {
                $.ajax({
                        type: "GET",
                        url: "/api/search-pg/",
                        data: "keyword="+keyword, 
                        dataType: "json",
                        success: function(data) {
                               var htmlresult = "";
                               mulitselectjm.var.searchdata = data;
                               if (data.length > 0) {
                                   for (i = 0; i < data.length; i++) { 
                                       console.log(data[i]['title1']);

                                       htmlresult+= '<div style="width: 100%; padding-top: 5px; min-height: 50px; border-bottom:1px solid #e8e8e8; margin-left:-1px; cursor: pointer;" onclick="mulitselectjm.selectItem('+i+','+"'"+textarea_id+"'"+');">';
                                       htmlresult+= "<div style='width: 100%; padding-left: 8px;'>";


                                       if(typeof  data[i]['title1'] != 'undefined'){
                                           icon = ''
                                           if (typeof  data[i]['icon'] != 'undefined') {
                                                icon = '<img src="'+data[i]['icon']+'" style="margin-top: -4px; filter: invert(1);">';
                                           }

                                           htmlresult+= "<div style='width: 100%; font-size:14px;'>"+icon+'&nbsp;'+data[i]['title1']+"</div>";
                                       }
                                       if(typeof  data[i]['title2'] != 'undefined') {
                                           htmlresult+= "<div style='width: 100%; font-size:12px;'>"+data[i]['title2']+"</div>";
                                       }
                                       if(typeof  data[i]['title3'] != 'undefined') {
                                           htmlresult+= "<div style='width: 100%; font-size:10px;'>"+data[i]['title3']+"</div>";
                                       }

                                       htmlresult+= "</div>";

                                       htmlresult+= "</div>";
                                       //if(typeof theObject['key'] != 'undefined'){
                                       //  
                                       //}
                                   }
                               }   else {
                                       htmlresult+= '<div>No results found.</div>';

                               }
                            // $("form#updatejob").hide(function(){$("div.success").fadeIn();}); 
                               $('#dropdown-multiselectjm-'+textarea_id).html("<div style='width: 100%'>"+htmlresult+"</div>");
                               $('#dropdown-multiselectjm-holder-'+textarea_id).slideDown('slow');

                        },
                        error: function(XMLHttpRequest, textStatus, errorThrown) { 
                            // alert("Status: " + textStatus); alert("Error: " + errorThrown); 
                        }       
                });
             }


	}
        

}
// mulitselectjm.init('id_task_owner');
