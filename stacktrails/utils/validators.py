from rest_framework import serializers
from typing import Any, Sequence


class ExtentionValidator:
    def __init__(self, extentions: Sequence) -> None:
        self.extentions = extentions

    def __call__(self, value) -> Any:
        *_, ext = value.name.split(".")
        if ext not in self.extentions:
            raise serializers.ValidationError("unsuppoted  extention")
