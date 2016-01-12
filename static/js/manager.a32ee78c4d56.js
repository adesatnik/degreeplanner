$(document).ready(function(){
	
	$(document).on("click", ".remove-plan", function(event){
		var id = event.target.id;
		var plan = id.split("-")[0];
		$.ajax({
			url:"/planner/removeplan/" + plan,
			type: "GET",
			dataType: "json",
			success: function(json){
				if (json.status == "success"){
					$("#" + plan +"-entry").remove();
					if ( $("#plans").text().trim() == ""){
						$("#plan-message").text("You have no plans. Add some!");
					}
				}
			}
		})
		
	})
	
	$("#addlink").click(function(event){
		$("#add-plan").show();
	})
	
	$("#add-plan").submit(function (event){
		event.preventDefault()
		$("#loading-wheel").show()
		$.ajax({
			url: "/planner/add/",
			type: "POST",
			data: $("#add-plan").serialize(),
			dataType: "json",
			success: function(json)
			{
				if(json.status == "success"){
					$("#loading-wheel").hide();
					$("#no-plans").remove();
					$("#plan-message").text("You have the following plans: ");
					$("#plans").append(json.new_plan);
					$("#add-plan").hide();
					
				}
				else{
					$("#loading-wheel").hide();

				}
				
			}
			
		})
	})
		
})
