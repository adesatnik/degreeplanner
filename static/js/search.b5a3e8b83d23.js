$(document).ready(function(){
	
	$("#form").submit(function(event){
		event.preventDefault()
		$("#loading-wheel").show()
		$("#results-wrapper").empty()
		$.ajax({
			url: "query/",
			type: "POST",
			data: $("#form").serialize(),
			dataType: "json",
			success: function(json){
				$("#loading-wheel").hide()
				$("#results-wrapper").append(json.results)
			}
		})
	})
		
	
})
