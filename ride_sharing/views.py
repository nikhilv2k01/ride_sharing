from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Ride
from .serializers import *
from .utils import *


class RideCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        mutable_data = request.data.copy()

        mutable_data["rider"] = request.user.id
        mutable_data["current_location"] = request.data.get(
            "pickup_location", None)
        serializer = RideCreateSerializer(data=mutable_data)
        if serializer.is_valid():
            ride = serializer.save()
            start_ride_tracking(ride.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response(
                {"message": "Ride does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = RideStatusUpdateSerializer(
            ride, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RideDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
            serializer = RideDetailSerializer(ride)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ride.DoesNotExist:
            return Response(
                {"message": "Ride does not exist."}, status=status.HTTP_404_NOT_FOUND
            )


class RideListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rides = Ride.objects.filter(rider=request.user)
        serializer = RideDetailSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RideLocationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
            serializer = RideLocationSerializer(ride)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ride.DoesNotExist:
            return Response({"message": "Ride does not exist."}, status=status.HTTP_404_NOT_FOUND)
