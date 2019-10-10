## Connect and read the data from the growatt front end, returning just the data we care about.

import requests 
from lxml import html
import sys
import json
import datetime

## A comment to make source control kick in...

## Setup a session for this work
Growatt_session = requests.session()

## Build the login details etc
payload = {
        
        "account":  "samCatBrowser",
        "password": "test123?",
        "validateCode": ""
}

login_url = "https://server.growatt.com/login"

result = Growatt_session.post(
	login_url, 
	data = payload, 
	headers = dict(referer=login_url)
)

# sys.stdout.write(chr(13)+chr(10)+"---------------------------------------------------------------------------"+chr(13)+chr(10))
# sys.stdout.write(chr(13)+chr(10)+"---------------------------------------------------------------------------"+chr(13)+chr(10))
# sys.stdout.write("Result of logging in:  " + result.text + chr(13)+chr(10))       # Debugging - result of login attempt
# print("Cookies:   ")
# print(Growatt_session.cookies.get_dict())

## Next we want to get the data we are after, call devices by plant which returns JSON
login_url = "https://server.growatt.com/panel/getDevicesByPlantList"

payload = {
        
        "currPage":  "1",
        "plantId": "40897"
}

result = Growatt_session.post(
    login_url,
    data = payload,
    headers = dict(referer=login_url)
)

## Consume the returned data
## Values updated every 5 minutes from when solar is generating, no point updating at night... 1 hour before sunrise to 1 hour after?


# sys.stdout.write(result.text)         # Write the full raw data received out, looks like JSON


growattData         = json.loads(result.text)
growattDataObj      = growattData["obj"]            # Json hence double quotes
growattDataObjDatas = growattDataObj['datas']       # Dict now, hence single quotes

growattCurrentPAC            = growattDataObjDatas[0]['pac']                # Current power
growattCurrentNominal_power  = growattDataObjDatas[0]['nominal_power']      # Maximum power
growattCurrentlastUpdateTime = growattDataObjDatas[0]['lastUpdateTime']     # Last Updated


# Weather from BBC section  #############################################################################################################################

## Setup a session for this work
BBC_session = requests.session()

#result = BBC_session.post("http://www.bbc.co.uk")
#result = BBC_session.post("https://www.bbc.co.uk/weather")
#result  = BBC_session.post("https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/2636002")

payload = {
        
        "Accept":	        "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding":	"gzip, deflate, br",
        "Accept-Language":	"en-GB,en;q=0.5",
        "Connection":	    "keep-alive",
        "DNT":	            1,
        "Host":	            "https://www.bbc.co.uk/weather",
        "Upgrade-Insecure-Requests":	1,
        "User-Agent":	    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
}

result = BBC_session.get("https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/2636002", data=payload, headers = dict(referer=login_url))


#sys.stdout.write(chr(13)+chr(10)+"---------------------------------------------------------------------------"+chr(13)+chr(10))
#print(result.text)
#sys.stdout.write(chr(13)+chr(10)+"---------------------------------------------------------------------------"+chr(13)+chr(10))

bbcData                = json.loads(result.text)
bbcDataForecasts       = bbcData["forecasts"]                    # Json hence double quotes
bbcDataForecastsToday  = bbcDataForecasts[0]                   # Dict now, hence single quotes
bbcDataForecastsTodaySummary        = bbcDataForecastsToday['summary']       # Dict now, hence single quotes
bbcDataForecastsTodaySummaryReport  = bbcDataForecastsTodaySummary['report'] # Dict now, hence single quotes

#print(bbcDataForecastsTodaySummaryReport)
#sys.stdout.write(chr(13)+chr(10)+"---------------------------------------------------------------------------"+chr(13)+chr(10))


weather_description          = bbcDataForecastsTodaySummaryReport['enhancedWeatherDescription']      # Wordy Weather Description
weather_sunrise              = bbcDataForecastsTodaySummaryReport['sunrise']                         # Wordy Weather Description
weather_sunset               = bbcDataForecastsTodaySummaryReport['sunset']                          # Wordy Weather Description


###############################################################################################################################################
# Output section  #############################################################################################################################

sys.stdout.write("---------------------------------------------------------------------------"+chr(13)+chr(10))
print(datetime.datetime.now())
sys.stdout.write("Weather: "+ weather_description + ".  Sunrise: " + weather_sunrise + "  Sunset: " + weather_sunset  + chr(13)+chr(10))
sys.stdout.write("Solar: Current Power: " + growattCurrentPAC + " W (" + growattCurrentNominal_power + " W max)" + chr(13)+chr(10))
sys.stdout.write("---------------------------------------------------------------------------"+chr(13)+chr(10))

###############################################################################################################################################
###############################################################################################################################################
