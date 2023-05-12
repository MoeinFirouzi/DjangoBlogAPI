from rest_framework import serializers
from blog.models import Post
from accounts.models import Author


class PostSerializer(serializers.ModelSerializer):
    post_url = serializers.SerializerMethodField(method_name="get_post_url")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "status",
            "create_time",
            "update_time",
            "author",
            "post_url",
        ]
        read_only_fields = ["author", "create_time", "update_time"]

    def create(self, validated_data):
        author = Author.objects.get(user=self.context.get("request").user)
        validated_data["author"] = author
        return super().create(validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["author"] = instance.author.user.email
        return ret

    def get_post_url(self, instance):
        instance_url = instance.get_absolute_url()
        return self.context["request"].build_absolute_uri(instance_url)
