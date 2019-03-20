var RESTAURANTS; // a list of dictionaries containing: image_url; google_url; name; address
var INDEX = 0;

console.log("Javascript is Running! YAY!");
//THESE ARE THE 3 EVENTS THAT ARE HANDLED
window.onload = function(){
	GetRestaurant(INDEX);
}
function NextPage(){
	GetRestaurant(INDEX +1);
}
function PrevPage(){
	GetRestaurant(INDEX -1);
}

function GetRestaurant(index){ 
	var xmlhttp = new XMLHttpRequest();
	var url = "/getmyplaces/"+index+"/";
	xmlhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			json_dict = JSON.parse(this.responseText);
			RESTAURANTS = json_dict.restaurants;
			console.log("Restaurant objects received from server, /getmyplaces/");
			console.log(this.responseText);
			if(json_dict.status == "ok"){
				INDEX = index;
				DisplayRestaurants();
			}
		}
	};
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
}
function DisplayRestaurants(){
	$( "#restaurants_container" ).children().remove();
	for (var i = 0; i < RESTAURANTS.length; i++) {
        	restaurant = RESTAURANTS[i];
		console.log("appending restaurant");
		console.log(restaurant.name);
		$( "#restaurants_container" ).append('<div id="restaurant">');
		$( "#restaurants_container" ).append('<strong><a id="restaurant_name" href="'+restaurant.google_url+'">'+restaurant.name+'</a></strong><br>');	
		$( "#restaurants_container" ).append('<img id="restaurant_image" src="'+restaurant.image_url+'">');
		$( "#restaurants_container" ).append('</div><br>');
		console.log("restaurant appended");
	}
}

