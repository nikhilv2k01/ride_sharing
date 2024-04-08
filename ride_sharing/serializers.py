from rest_framework import serializers
from .models import Ride


class RideCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = (
            "id",
            "rider",
            "pickup_location",
            "dropoff_location",
            "current_location",
            "status",
        )


class RideStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ("id", "status")

    def validate(self, data):
        ride = self.instance
        status = data.get("status")

        if ride.status == "REQUESTED":
            if status not in ["STARTED", "CANCELLED"]:
                raise serializers.ValidationError(
                    "Invalid status transition. Status can only be changed to 'started' or 'cancelled'."
                )

        elif ride.status == "STARTED":
            if status not in ["COMPLETED", "CANCELLED"]:
                raise serializers.ValidationError(
                    "Invalid status transition. Status can only be changed to 'completed' or 'cancelled'."
                )

        elif ride.status in ["COMPLETED"]:
            raise serializers.ValidationError(
                "Ride cannot be updated. Status is already 'completed'"
            )

        elif ride.status in ["CANCELLED"]:
            raise serializers.ValidationError(
                "Ride cannot be updated. Status is already 'cancelled'"
            )

        return data

    # def update(self, instance, validated_data):
    #     instance = super().update(instance, validated_data)

    #     # Check if the ride status is "COMPLETED" or "CANCELLED"
    #     if instance.status in ["COMPLETED", "CANCELLED"]:
    #         stop_ride_tracking(instance.id)  # Stop ride tracking

    #     return instance


class RideDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = "__all__"


class RideLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ("id", "current_location_lat", "current_location_lon")
