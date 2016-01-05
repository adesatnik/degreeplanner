$(document).ready(function() {
	$.ajax({
		url: "getdmajors",
		type: "GET",
		dataType: "json",
		success: function(json){
			$("#loading-wheel").hide()
			$("#declared-majors-wrapper").append(json.major_data)
		}
	})
// Icons
	
	$(document).on({
		mouseenter: function(event){
		var id = event.target.id;
		var _class = id.split("-")[0]
		$("#" + _class + "-deletecontainer").show()			
		},
		mouseleave: function(event){
		var id = event.target.id;
		var _class = id.split("-")[0]
		$("#" + _class + "-deletecontainer").hide()			
		}
	}, ".class-container");
	
	
	$(document).on({
		mouseenter: function(event){
		var id = event.target.id;
		var quarter = id.split("-")[0] + "-" + id.split("-")[1]
		$("#" + quarter + "-add").show()			
		},
		mouseleave: function(event){
		var id = event.target.id;
		var quarter = id.split("-")[0] + "-" + id.split("-")[1]
		$("#" + quarter + "-add").hide()			
		}
	}, ".quarter");
	
	

//Dropdown menu logic
	$(document).on("click", ".major-title",function (event){
		var id = event.target.id;
		var major = id.split("_")[0];
		$("#" + major + "_requirements").toggle();
	});
	
	$(document).on("click", ".requirement-title",function (event){
		var id = event.target.id;
		var requirement = id.split("_")[0] + "_" + id.split("_")[1] ;
		$("#" + requirement + "_contents").toggle();
		
	});
	
//Delete classes AJAX
	$(document).on("click", ".delete-link", function (event){
		var id = event.target.id;
		var class_id = id.split("-")[0];
		$("#declared-majors").remove()
		$("#loading-wheel").show()
		$.ajax({
			url:"delete/" + class_id,
			type: "GET",
			dataType: "json",
			success: function(json){
				$("#loading-wheel").hide()
				$("#declared-majors-wrapper").append(json.major_data)
				$('#plan-table').remove()
				$('#plan-table-wrapper').append(json.plan_table)
			}
			
		})
	})	

//Delete declared major AJAX
	$(document).on("click", ".major-remove", function(event){
		var id = event.target.id;
		var major_id = id.split("-")[0];
		$("#declared-majors").remove()
		$("#loading-wheel").show()
		$.ajax({
			url:"removedmajor/" + major_id,
			type: "GET",
			dataType: "json",
			success: function(json){
				$("#loading-wheel").hide()
				$("#declared-majors-wrapper").append(json.major_data)
			}
		})
	})

//Add major AJAX
	$("#declaremajor").submit(function (event){
		event.preventDefault()
		$("#declared-majors").remove()
		$("#loading-wheel").show()
		$.ajax({
			url:"adddmajor/",
			type: "POST",
			data: $("#declaremajor").serialize(),
			success: function(json)
			{
				$("#loading-wheel").hide()
				$("#declared-majors-wrapper").append(json.major_data)
			}
		});
	})
	
});
