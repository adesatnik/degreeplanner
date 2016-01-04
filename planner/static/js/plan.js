$(document).ready(function() {
// Icons
	$(".class-container").hover(function (event){
		var id = event.target.id;
		var _class = id.split("-")[0]
		$("#" + _class + "-delete").toggle()
	})
	
	$(".quarter").hover(function (event){
		var id = event.target.id;
		var quarter = id.split("-")[0] + "-" + id.split("-")[1]
		$("#" + quarter + "-add").toggle()
	})
	
	

//Dropdown menu logic
	$(".major-title").click(function (event){
		var id = event.target.id;
		var major = id.split("_")[0];
		$("#" + major + "_requirements").toggle();
	});
	
	$(".requirement-title").click(function (event){
		var id = event.target.id;
		var requirement = id.split("_")[0] + "_" + id.split("_")[1] ;
		$("#" + requirement + "_contents").toggle();
		
	});
	


	
});
