from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from geopy.distance import distance
from .models import City
from .serializers import CitySerializer
from .coordinates import get_city_coordinates


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def perform_create(self, serializer):
        city_name = serializer.validated_data['name']
        latitude, longitude = get_city_coordinates(city_name)
        serializer.save(latitude=latitude, longitude=longitude)

    @action(detail=False, methods=['get'], url_path='nearest-cities')
    def nearest_cities(self, request):
        try:
            latitude = float(request.query_params.get('latitude'))
            longitude = float(request.query_params.get('longitude'))
        except (TypeError, ValueError):
            return Response({"error": "Invalid latitude or longitude format."}, status=status.HTTP_400_BAD_REQUEST)

        cities = City.objects.all()
        if not cities:
            return Response({"error": "No cities found."}, status=status.HTTP_404_NOT_FOUND)

        cities_with_distances = [
            (city, distance((latitude, longitude), (city.latitude, city.longitude)).km)
            for city in cities
        ]
        cities_with_distances.sort(key=lambda x: x[1])

        nearest_cities = cities_with_distances[:2]  # Get the two nearest cities
        serializer = CitySerializer([city for city, dist in nearest_cities], many=True)
        return Response(serializer.data)
