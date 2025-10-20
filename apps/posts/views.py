from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.posts.models import AuthorModel, FollowModel
from apps.posts.serializers import PostSerializer, FollowerSerializer, CommentSerializer

from apps.posts.models import PostModel, CommentModel
from apps.posts.serializers import PostUpdateSerializer, CommentUpdateSerializer


class PostView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def post(self,request):
        author = AuthorModel.objects.get(user=request.user)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=author)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        posts = PostModel.objects.all().order_by('created_at')
        serializer = self.serializer_class(posts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class FollowerView(APIView):
    serializer_class = FollowerSerializer

    def get(self,request):
        following = FollowModel.objects.all().order_by('following_id')
        followers = FollowModel.objects.all().order_by('follower_id')

        following_serializer = self.serializer_class(following,many=True)
        followers_serializer = self.serializer_class(followers,many=True)

        data = {
            'following': following_serializer.data,
            'followers': followers_serializer.data,
        }

        return Response(data,status=status.HTTP_200_OK)

class CommentsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request):
        author = AuthorModel.objects.get(user=request.user)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        comments = CommentModel.objects.all().order_by('created_at')
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostUpdateSerializer

    def put(self, request, pk):
        try:
            post = PostModel.objects.get(pk=pk, author__user=request.user)
        except PostModel.DoesNotExist:
            return Response(data={"error": "Post not found or not owned by you"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            post = PostModel.objects.get(pk=pk, author__user=request.user)
        except PostModel.DoesNotExist:
            return Response(data={"error": "Post not found or not owned by you"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        try:
            post = PostModel.objects.get(pk=pk, author__user=request.user)
        except PostModel.DoesNotExist:
            return Response(data={"error": "Post not found or not owned by you"}, status=status.HTTP_404_NOT_FOUND)

        post.delete()
        return Response(data={"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class CommentUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentUpdateSerializer

    def put(self, request, pk):
        try:
            comment = CommentModel.objects.get(pk=pk, author__user=request.user)
        except CommentModel.DoesNotExist:
            return Response(data={"error": "Comment not found or not owned by you"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            comment = CommentModel.objects.get(pk=pk, author__user=request.user)
        except CommentModel.DoesNotExist:
            return Response(data={"error": "Comment not found or not owned by you"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @staticmethod
    def delete(request, pk):
        try:
            comment = CommentModel.objects.get(pk=pk, author__user=request.user)
        except CommentModel.DoesNotExist:
            return Response(data={"error": "Comment not found or not owned by you"}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response(data={"message": "Comment deleted successfully"}, status=status.HTTP_403_FORBIDDEN)
