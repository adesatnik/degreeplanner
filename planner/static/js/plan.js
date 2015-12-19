$(document).ready(function() {
	//Initializes popovers
	$(function () {
  		$('[data-toggle="popover"]').popover()
	})
	
	// Popover logic
	var active = "none";
	$(".quarter").click(function (event){
		var id = event.target.id
		var year = id.split("-")[0]
		var quarter = id.split("-")[1]
		
		if ($("#"+ year + "-" + quarter + "-" +"text").is(":empty")){
			if (active == year + "-"+ quarter){
				$("#"+ year + "-" + quarter + "-" +"p").popover("hide")
				active = "none"
			}
			else if (active == "none"){
				$("#"+ year + "-" + quarter + "-" +"p").popover("show")	
				active = year + "-" + quarter

			}
		}
	});
	
	$(".textquarter").click(function (event){
		var id = event.target.id
		var year = id.split("-")[0]
		var quarter = id.split("-")[1]
		if (!$("#"+ year + "-" + quarter + "-" +"text").is(":empty")){

			if (active == year + "-"+ quarter){
				$("#"+ year + "-" + quarter + "-" +"p").popover("hide")
				active = "none"
			}
			else if (active == "none"){
				$("#"+ year + "-" + quarter + "-" +"p").popover("show")	
				active = year + "-" + quarter
			}
		}
		

		
	});
	
	$("body").click(function (event){
				if(delete_activated != "none"){
			$("." + delete_activated + "-class").click(function (event) {
				$.get( "delete/" + event.target.id, function( data ) {
				});
				event.target.remove();
				delete_activated = "none";
			})
		}
	})
	 
	var delete_activated = "none";
	$(document).on("click", ".delete-button", function (event){
		var id = event.target.id
		var year = id.split("-")[0]
		var quarter = id.split("-")[1]
		
		$("." + year + "-" + quarter + "-class").wrap("<a href='#'></a>");
		delete_activated = year + "-" + quarter 
	});
	

	


	
});
