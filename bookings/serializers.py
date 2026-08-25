from rest_framework import serializers
from .models import BookingRequest

class BookingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingRequest
        fields = ("teacher_subject" , "proposed_price" , "message")



class BookingListSerializer(serializers.ModelSerializer):

    teacher = serializers.CharField(source =  "teacher_subject.subject.name" , read_only = True) 

    class Meta:
        model = BookingRequest
        fields = (
            "id",
            "teacher",
            "proposed_price",
            "status",
            "created_at",
        )



class BookingDetailSerializer(serializers.ModelSerializer):

    """

    """

    student  =  serializers.CharField(source = "student.get_full_name" , read_only = True)
    teacher = serializers.CharField(source = "teacher_subject.teacher.user.get_full_name" , read_only = True)
    subject = serializers.CharField(source = "teacher_subject.subject.name" , read_only = True)

    class Meta:
        model = BookingRequest
        fields = "__all__   "