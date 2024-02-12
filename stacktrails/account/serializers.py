from rest_framework import serializers


from .models import UserProfile, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ["user"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, required=False)

    class Meta:
        model = User
        exclude = [
            "last_login",
            "is_staff",
            "is_superuser",
            "user_permissions",
            "groups",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def to_representation(self, instance):
        resp = super().to_representation(instance)
        profile = resp.pop("profile", None)
        if isinstance(profile, dict):
            profile.pop("id", None)
            profile.pop("user", None)
            resp.update({**profile})
        return resp
