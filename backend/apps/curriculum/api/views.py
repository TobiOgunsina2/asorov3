from rest_framework import generics, permissions
from rest_framework.views import APIView, Response

from curriculum.models import Unit
from curriculum.api.serializers import LessonSerializer, ReviewSlideSerializer, UnitSerializer

from curriculum.services import build_lesson_payload, get_practice_review_data

# Create your views here.

class UnitList(generics.ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]

class LessonView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, lesson_code):
        user = request.user

        lesson, review_data = build_lesson_payload(user, lesson_code)
        review_slides = ReviewSlideSerializer(
            review_data,
            many=True
        ).data

        data = LessonSerializer(lesson).data
        data["review_slides"] = review_slides

        return Response(data)

class ReviewLessonView(APIView):
    def get(self, request):
        user = request.user
        review_data = get_practice_review_data(user)
        
        data = ReviewSlideSerializer(review_data, many=True).data

        return Response(data)
