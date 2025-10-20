from rest_framework import serializers

from apps.posts.models import AuthorModel, PostModel, FollowModel, CommentModel


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['id','message','created_at']
        extra_kwargs = ['is_active']

        @staticmethod
        def validate(attrs):
            if len(attrs) < 100:
                raise serializers.ValidationError("Post length should not be less than 100")
            return attrs


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowModel
        fields = ['id','follower','following','followed_at']
        extra_kwargs = ['is_active']


class AuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    email = serializers.EmailField(source='user.username',read_only=True)
    posts = PostSerializer(many=True,read_only=True)
    followers = serializers.SerializerMethodField(many=True,read_only=True)
    following = serializers.SerializerMethodField(many=True,read_only=True)

    class Meta:
        model = AuthorModel
        fields = ['id','username','email','avatar','posts','followers','following','created_at','updated_at']
        extra_kwargs = ['is_active']

        @staticmethod
        def get_followers(obj):
            for follow in obj.followers.all():
                return follow.user.username
            return None

        @staticmethod
        def get_following(obj):
            for follow in obj.following.all():
                return follow.user.username
            return None


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    post = PostSerializer(many=True,read_only=True)

    class Meta:
        model = CommentModel
        fields = ['id','author','post','text','is_approved']
        extra_kwargs = ['is_active']

        @staticmethod
        def validate_text(value):
            if len(value.strip()) < 3:
                raise serializers.ValidationError("The comment must be at least 3 characters long")
            return value

from rest_framework import serializers
from apps.posts.models import PostModel, CommentModel


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['id', 'message', 'is_published']

    @staticmethod
    def validate_message(value):
        if not value.strip():
            raise serializers.ValidationError("Message must not be empty")
        return value


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['id', 'text', 'is_approved']

    @staticmethod
    def validate_text(value):
        if not value.strip():
            raise serializers.ValidationError("Comment text must not be empty")
        return value

