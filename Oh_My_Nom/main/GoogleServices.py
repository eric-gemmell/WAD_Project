import requests
from ipware import get_client_ip

#Token required in order to access ipinfo website and get location services
IPINFO_TOKEN = "4e2d644d3f142c"

#Token required in order to access Google Maps API
GOOGLE_MAPS_TOKEN = "AIzaSyBh9dpjyfekYl-JZWsqJh78mRq4m3_0GBM"


def GetLocationFromIP(ipAddress="85.255.236.243"):
        #Returns a Dictionary containing the approximate latitude and longitude using the ip address provided
	#Please Note that this function is very approximate in function
	if(ipAddress != ""):
		ipAddress = "/"+ipAddress
	url = "http://ipinfo.io{}/json?token={}".format(ipAddress,IPINFO_TOKEN)
	response = requests.get(url)
	response_dict = response.json()
	result = {"status":"ok"}
	if("loc" not in response_dict or "city" not in response_dict):
		#If the ip provided does not yield a location, often as a result of being a local ip address
		# the location of this server will be provided instead
		result["status"] = "not ok"
		url = "http://ipinfo.io/json?token={}".format(IPINFO_TOKEN)
		response = requests.get(url)
		response_dict = response.json()
	result["location"] = response_dict["loc"].split(",")
	result["address"] = response_dict["city"]
	return result


def GetLocationFromText(address = "G206NB"):
	url = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}"
		"&inputtype=textquery&fields=geometry,formatted_address&key={}").format(address,GOOGLE_MAPS_TOKEN)
	response = requests.get(url)
	response_dict = response.json()
	result = {"status":"ok"}
	location = []
	if(len(response_dict["candidates"]) > 0):
		location.append(str(response_dict["candidates"][0]["geometry"]["location"]["lat"]))
		location.append(str(response_dict["candidates"][0]["geometry"]["location"]["lng"]))
		result["location"] = location
		result["address"] = str(response_dict["candidates"][0]["formatted_address"])
	else:
		result["status"] = "not ok"
	return result

	
def RestaurantInfoDictFromGoogleResponse(GoogleResponse):
    #Takes in a part of the response dict corresponding to ONE restaurant,
    #Returns a Dictionary Containing only the necessary information
    result = {}#The dictionary to be returned containing restaurant information
    if("name" not in GoogleResponse):
        #Deal Braker! Cannot return a restaurant without a name...
        return None
    if("vicinity" not in GoogleResponse):
        #Deal Braker! Cannot return a restaurant without an address
        return None
    if("place_id" not in GoogleResponse):
        #Deal Braker! Cannot return a restaurant that has no additional info on google...
        return None
    result["name"] = GoogleResponse["name"]
    result["address"] = GoogleResponse["vicinity"]
    result["google_url"] = "https://www.google.com/maps/place/?q=place_id:{}".format(GoogleResponse["place_id"])
    result["place_id"] = GoogleResponse["place_id"]    
    result["image_url"] = "/static/images/main.png"
    if("photos" in GoogleResponse):
        photo_reference = GoogleResponse["photos"][0]["photo_reference"]
        result["image_url"] = ("https://maps.googleapis.com/maps/api/place/photo?maxwidth=400"
                     "&photoreference={}&sensor=false&key={}").format(photo_reference,GOOGLE_MAPS_TOKEN)
    return result
    

def GetRestaurantsFromLocation(location = ['55.8723715', '-4.2826219']):
        url = ("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}"
                "&rankby=distance&type=restaurant&key={}").format(location[0],location[1],GOOGLE_MAPS_TOKEN)
        response = requests.get(url)
        response_dict = response.json()
        result = []#The List of Dictionarys containing restaurant information that will be returned
        for RestaurantInfo in response_dict["results"]:
            result.append(RestaurantInfoDictFromGoogleResponse(RestaurantInfo))
        return result


def GetRestaurantFromPlace_ID(place_id = "ChIJxwP9GjJEiEgRps-HjBk6lPk"):
	#returns a dictionary containing, an image url, a name, the address, the place_id, the google_maps url
	#and a status code indicating all is okay
	url = ("https://maps.googleapis.com/maps/api/place/details/json?placeid={}"
		"&fields=name,vicinity,photo,place_id&key={}").format(place_id,GOOGLE_MAPS_TOKEN)
	response = requests.get(url)
	response_dict = response.json()
	result = RestaurantInfoDictFromGoogleResponse(response["result"])
	if(result == None):
		return {"status":"not ok"}
	else:
		result["status"] = "ok"
		return result 


def GetRequestIP(request):
	ip, is_routable = get_client_ip(request)
	if ip is None:
		# Unable to get the client's IP address
		pass
	else:
    		# We got the client's IP address
		pass
	if is_routable:
        	# The client's IP address is publicly routable on the Internet
		pass
	else:
		pass
	return ip


import json
def GetLocation(request):
	#returns a dictionary containing the location in latitude and longitude
	#and a message describing the location and whether we were succesful in getting it or not
	
	location_message = ""
	
	#try to get location from text input
	if request.method == "POST":
		try:
			json_dict = json.loads(request.body.decode("utf-8"))
		except:
			return {"error":"poor request"}
		
		if("location_text" in json_dict):
			print(json_dict["location_text"])
			print(type(json_dict["location_text"]))
			if(json_dict["location_text"] != "undefined"):
				location_dict = GetLocationFromText(address = json_dict["location_text"])
				if(location_dict["status"] != "ok"):
					location_message = "Sorry, but we could not find the place '{}'".format(json_dict["location_text"])
				else:
					return {"location":location_dict["location"],"location_message":"Using '{}' as your location".format(location_dict["address"])}
	
	#Try to get user information 
	if request.user.is_authenticated:
		try:
			input_location = request.user.userinfo.location
		except:
			input_location = ""

		if(input_location != ""):
			location_dict = GetLocationFromText(address = input_location)
			if(location_dict["status"] != "ok"):
				if(location_message == ""):
					location_message = "Sorry, but your saved address '{}' could not be found".format(input_location)
				else:
					location_message += "\nYour saved address '{}' couldn't be found either".format(input_location)	
			else:
				return {"location":location_dict["location"],"location_message":"Using '{}' as your location".format(location_dict["address"])}
		else:
			if (location_message == ""):
				location_message = "No address is saved under this account"
			else:
				location_message +="\nNor is there any address saved in this account"

	#lastly use ip to get address
	ip = GetRequestIP(request)
	location_dict = GetLocationFromIP(ipAddress = ip)
	if(location_dict["status"] != "ok"):
		#Ip failed us so using default address
		location_dict = GetLocationFromText()
		if location_message != "":
			location_message += "\nWe also couldn't estimate your location, so we are using the default '{}'".format(location_dict["address"])
		else:
			location_message = "We could not estimate your location, we are using the default '{}'".format(location_dict["address"])
		return {"location":location_dict["location"],"location_message":location_message}
	else:
		return {"location":location_dict["location"],"location_message":"Using '{}' as your location".format(location_dict["address"])}

