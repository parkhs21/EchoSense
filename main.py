import json
import openai
from openai import OpenAI
import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

client = OpenAI(api_key=os.getenv["OPENAI_API_KEY"])

def fetch_customer_profile(user_id):
    #실제 API 호출로 대체 가능//임시로 해놨음...
    if user_id == "user1":
        return {
            "name": "YIB",
            "location": {
                "lat": 37.556838,
                "long": 126.923774,
            },
            "preferences": {
                "food": ["Italian", "Chinese", "Japanese"],
                "activity": ["Reading", "Hiking", "Swimming"]
            },
            "recent_searches": ["Italian restaurants", "Book stores"]
        }
    else:
        return None

def get_place_details(place_id, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&language=ko&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        result = json.loads(response.content)["result"]
        return result
    else:
        print(f"Google Places API request failed with {response.status_code}")
        print(f"Response content: {response.content}")
        return None

def call_google_place_api(user_id, place_type, food_preference=None):
    try:
        customer_profile = fetch_customer_profile(user_id)
        #위치기반 추천
        lat = customer_profile["location"]["lat"]
        lng = customer_profile["location"]["long"]
        
        API_KEY = os.getenv["GOOGLE_PLACES_API_KEY"]
        LOCATION = f"{lat},{lng}"
        RADIUS = "1000"
        TYPE = place_type
        
        if place_type == "restaurant" and food_preference:
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={LOCATION}&radius={RADIUS}&type={TYPE}&keyword={food_preference}&language=ko&key={API_KEY}"
        else:
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={LOCATION}&radius={RADIUS}&type={TYPE}&language=ko&key={API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            results = json.loads(response.content)["results"]
            places = []
            for place in results[:2]: #상위 2개만
                place_id = place["place_id"]
                place_details = get_place_details(place_id, API_KEY) #상세정보 가져오기
                
                place_name = place_details.get("name","N/A")
                place_types = next((t for t in place_details.get("types",[]) 
                                    if t not in ["food","point_of_interest"]),"N/A") #food, point_of_interest 제외
                place_rating = place_details.get("rating","N/A") #평점
                total_ratings = place_details.get("user_ratings_total","N/A") #총 리뷰 수
                place_address = place_details.get("vicinity","N/A") #주소
                
                if ',' in place_address:
                    street_address = place_address.split(',')[0] #주소가 ,로 구분되어 있을 경우 첫번째만 가져오기
                else:
                    street_address = place_address
                    
                place_info = f"{place_name}은 {place_types}이며 {place_rating}점을 받았습니다. {total_ratings}개의 리뷰가 있습니다. {street_address}에 위치해 있습니다."
                
                places.append(place_info)
                
            return places
        else:
            print(f"Google Places API request failed with {response.status_code}")
            print(f"Response content: {response.content}")
            return []
    except Exception as e:
        print(f"Error Google Place API: {e}")
        return []

def provide_user_specific_recommendations(user_input, user_id):
    customer_profile = fetch_customer_profile(user_id)
    
    customer_profile_str = json.dumps(customer_profile)
    food_preferences = customer_profile.get('preferences',{}).get('food',[])[0] if customer_profile.get('preferences',{}).get('food',[]) else None
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"너는 사용자의 의도를 감지하고 해석하는 정교한 어시스턴트 ai야. 너는 사용자의 요구가 간접적이거나 직접적인 방식으로 표현되더라도 이를 인지하고 해석할 수 있어야 해. 예를 들어 사용자가 '음식점 추천해줘'라고 말하면 사용자의 위치를 기반으로 음식점을 추천해줘야 해. 사용자가 '피곤하다','지쳤다'고 표현하거나 장거리 여행에 대해 언급하면 호텔같은 숙박옵션을 요청하는 것으로 해석하면 돼. 사용자의 요구가 불분명하거나 여러가지로 해석된다면 추가 설명을 요청해. {customer_profile_str}고객 프로필에서 확인할 수 있는 사용자의 선호도와 과거 경험을 바탕으로 맞춤형 답변을 제공하면 돼. "
            },
            {"role": "user", "content": user_input}
        ],
        temperature=0,
        functions=[
            {
                "name":"call_google_place_api",
                "description":"Google Place API를 호출하여 특정 위치 근처에서 특정 유형의 인기 장소를 찾는다. 사용자가 요구사항을 말하거나 장소를 찾고자 할 때 사용할 수 있다.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "place_type": {
                            "type":"string",
                            "description":"장소 유형"
                        }
                    }
                },
                "result":{
                    "type":"array",
                    "items":{
                        "type":"string"
                    }
                }
            }
        ],
    )
    
    print(response.choices[0].message.function_call)
    
    if response.choices[0].finish_reason=='function_call':
        function_call = response.choices[0].message.function_call
        if function_call.name == "call_google_place_api":
            place_type = json.loads(function_call.arguments)["place_type"]
            places = call_google_place_api(user_id, place_type, food_preferences)
            if places:
                return f"제가 추천드리는 장소는 {' '.join(places)}"
            else:
                return "죄송합니다. 장소를 찾을 수 없습니다."
            
    return "죄송합니다. 요청을 처리할 수 없습니다."
            
user_id = "user1"
user_input = "비오는 날에는 갈 곳 추천해줘"
output = provide_user_specific_recommendations(user_input, user_id)
print(output)