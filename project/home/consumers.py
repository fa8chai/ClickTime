import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Like, Post, Comment
from profile.models import Profile
import uuid




class PostConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'Post_{self.room_name}'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        #Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == 'like':
            id = text_data_json['post_id']
            username = text_data_json['username']
            # get the post from database
            try:
                val = uuid.UUID(id, version=4)
                post = Post.objects.get(pk = id)
            except (ValueError, Post.DoesNotExist):
                raise ValueError("Post not found")            
            
            # get user profile
            try:
                user = Profile.objects.get(username = username)
            except Profile.DoesNotExist:
                raise ValueError("user not found")            
            like, created = Like.objects.get_or_create(user = user , post = post)
            
            if not created:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'liked',
                    }
                )
            else:
                like.save()
                likes = post.likes.count()
                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'post_like',
                        'message':likes
                    }
                )


        elif message == 'dislike':
            id = text_data_json['post_id']
            username = text_data_json['username']
            # get the post from database
            try:
                val = uuid.UUID(id, version=4)
                post = Post.objects.get(pk = id)
            except (ValueError, Post.DoesNotExist):
                raise ValueError("Post not found")            
            
            # get user profile
            try:
                user = Profile.objects.get(username = username)
            except Profile.DoesNotExist:
                raise ValueError("user not found") 
            # get like object
            like = Like.objects.get(user = user, post= post)
            like.delete()
            likes = post.likes.count()
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'post_dislike',
                    'message':likes
                }
        )
        elif message == 'comment':
            comment = text_data_json['comment']
            post_id = text_data_json['post_id']
            username = text_data_json['username']
            # get post
            try:
                val = uuid.UUID(post_id, version=4)
                post = Post.objects.get(pk = post_id)
            except (ValueError, Post.DoesNotExist):
                raise ValueError("Post not found")            
            
            # get user profile
            try:
                user = Profile.objects.get(username = username)
            except Profile.DoesNotExist:
                raise ValueError("user not found") 
            # create comment object
            new_comment = Comment.objects.create(user = user, post = post, text = comment)
            new_comment.save()

            # send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'post_comment',
                    'message': new_comment
                }
            )

        else:
            raise ValueError("No handler for this message")
    
    # Receive message from room group
    def post_like(self, event):
        likes = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message':'like',
            'likes': likes,
            'hi':'hi'
        }))

    def liked(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message':'liked',
        }))

    def post_dislike(self, event):
        likes = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message':'dislike',
            'likes': likes
        }))

    def post_comment(self, event):
        comment = event['message']

        # send message to WebSocket
        self.send(text_data=json.dumps({
            'message':'comment',
            'user':comment.user.username,
            'created_on': comment.created_on.strftime("%I:%M %p %d %b") ,
            'text':comment.text,
            'img':comment.user.picture_url
        },indent=2, sort_keys=True, default=str) 
        )

        
        
        