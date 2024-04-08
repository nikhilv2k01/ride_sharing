# tasks.py
from celery import shared_task
from .models import Ride
from math import radians, sin, cos, sqrt, atan2


# Constants for simplicity (should be adjusted based on real-world scenario)
SPEED = 10  # Constant speed in meters per second
DIRECTION = 45  # Constant direction in degrees (e.g., 45 degrees)

# Function to calculate distance between two points
def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Haversine formula to calculate distance between two points on Earth's surface
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    R = 6371000.0  # Radius of the Earth in meters
    distance = R * c  # Distance in meters

    return distance

# Function to calculate new location based on movement
def calculate_new_location(current_lat, current_lon, speed, direction):
    # Convert direction from degrees to radians
    direction_rad = radians(direction)

    # Calculate new latitude and longitude based on speed and direction
    new_lat = current_lat + (speed / 111111) * sin(direction_rad)  # 1 degree of latitude is approximately 111111 meters
    new_lon = current_lon + (speed / (111111 * cos(current_lat))) * cos(direction_rad)

    return new_lat, new_lon

# Celery task definition
@shared_task
def update_ride_location(ride_id):
    print("update ride location------------------", ride_id)
    ride = Ride.objects.get(id=ride_id) 
    if ride.status ==  "STARTED":
        current_lat = ride.current_location.get('lat')  
        current_lon = ride.current_location.get('lng')  
        pickup_lat = ride.pickup_location.get('lat')  
        pickup_lon = ride.pickup_location.get('lng')  
        dropoff_lat = ride.dropoff_location.get('lat')   
        dropoff_lon = ride.dropoff_location.get('lng')
        
        # Check if latitude and longitude values are not None
        if current_lat is not None and current_lon is not None and \
           pickup_lat is not None and pickup_lon is not None and \
           dropoff_lat is not None and dropoff_lon is not None:
            # Calculate distance between current location and dropoff location
            distance_to_dropoff = calculate_distance(current_lat, current_lon, dropoff_lat, dropoff_lon)
            print(distance_to_dropoff , SPEED)
            if distance_to_dropoff > SPEED:  # If distance to dropoff is greater than speed, continue moving
                # Calculate new location towards dropoff location
                new_lat, new_lon = calculate_new_location(current_lat, current_lon, SPEED, DIRECTION)
                ride.current_location = {'lat': new_lat, 'lng': new_lon}  # Update current location as dictionary
                print("working", ride.current_location)
                ride.save()
            else:  # If distance is less than speed, ride has reached destination
                ride.status = 'COMPLETED'
                ride.save()
        else:
            print("Latitude or longitude missing in current_location, pickup_location, or dropoff_location.")
