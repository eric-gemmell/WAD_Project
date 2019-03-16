import requests

#Token required in order to access ipinfo website and get location services
IPINFO_TOKEN = "4e2d644d3f142c"

#Token required in order to access Google Maps API
GOOGLE_MAPS_TOKEN = "AIzaSyBh9dpjyfekYl-JZWsqJh78mRq4m3_0GBM"


def GetLocationFromIP(ipAddress="85.255.236.243"):
        #Returns a List containing the approximate latitude and longitude using the ip address provided
	#Please Note that this function is very approximate in function
        if(ipAddress != ""):
                ipAddress = "/"+ipAddress
        url = "http://ipinfo.io{}/json?token={}".format(ipAddress,IPINFO_TOKEN)
        response = requests.get(url)
        response_dict = response.json()
        return(response_dict["loc"].split(","))


def GetLocationFromText(address = "G206NB"):
        url = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}"
                "&inputtype=textquery&fields=geometry&key={}").format(address,GOOGLE_MAPS_TOKEN)
        response = requests.get(url)
        response_dict = response.json()
        location = []
        location.append(str(response_dict["candidates"][0]["geometry"]["location"]["lat"]))
        location.append(str(response_dict["candidates"][0]["geometry"]["location"]["lng"]))
        return location

	
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
    
    result["image_url"] = "ImageMissing!"
    if("photos" in GoogleResponse):
        photo_reference = GoogleResponse["photos"][0]["photo_reference"]
        result["image_url"] = ("https://maps.googleapis.com/maps/api/place/photo?maxwidth=400"
                     "&photoreference={}&sensor=false&key={}").format(photo_reference,GOOGLE_MAPS_TOKEN)
    return result
    

def GetRestaurantsFromLocation(restaurantNumber = 3,location = ['55.8723715', '-4.2826219']):
        url = ("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}"
                "&rankby=distance&type=restaurant&key={}").format(location[0],location[1],GOOGLE_MAPS_TOKEN)
        response = requests.get(url)
        response_dict = response.json()
        result = []#The List of Dictionarys containing restaurant information that will be returned
        for RestaurantInfo in response_dict["results"]:
            result.append(RestaurantInfoDictFromGoogleResponse(RestaurantInfo))
        return result


def GetRequestIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
