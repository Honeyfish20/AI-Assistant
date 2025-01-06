from rest_framework import viewsets
from rest_framework.views import APIView, View
import json
from asgiref.sync import sync_to_async
from asyncio import ensure_future
import asyncio

from .models import UserPrompt
from .serializers import UserPromptSerializer
from .bedrock_utils import streaming_chat_feishu
from .feishu_utils import AESCipher, TokenManager, LarkMsgSender

from django.http import StreamingHttpResponse, HttpResponse, JsonResponse

class UserPromptViewSet(viewsets.ModelViewSet):
    queryset = UserPrompt.objects.all()
    serializer_class = UserPromptSerializer
    

        
# Feishu setting 
app_id = "cli_a692712a82799013"
app_secret = "X8qGkLY9jV5kRVhmsOcTEbP8lc7TGbv2"
verification_token = "3X6wZbD6eYlLp0xMSC6gnd76GJqRNBfB"
encryption_key = "XwIEv6YHtsccvLjramOD4gTI3IzKxuJU"

cipher = AESCipher(encryption_key)
users_info = {}
token_manager = TokenManager(app_id=app_id, app_secret=app_secret)
sender = LarkMsgSender(token_manager)
        
class ChatFeishuView(View):
    permission_classes = []

    async def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        cipher = AESCipher(encryption_key)

        try:
            parsed_data = json.loads(cipher.decrypt_string(data['encrypt']))
        except:
            return HttpResponse('Parsing Error')

        if 'challenge' in parsed_data:
            return JsonResponse({'challenge': parsed_data['challenge']})

        if 'event' in parsed_data and 'message' in parsed_data['event'] and 'content' in parsed_data['event']['message']:
            content = json.loads(parsed_data['event']['message']['content'])
            
            if 'text' in content:
                user_id = parsed_data['event']['sender']['sender_id']['user_id']
                user_prompt = await sync_to_async(UserPrompt.objects.get, thread_sensitive=True)(id=1)
                prompt = content['text']
                messages = []
                messages.append({"role": "user", "content": prompt})
                model_id = await sync_to_async(lambda: user_prompt.model_id.model_id, thread_sensitive=True)()
                model_region = await sync_to_async(lambda: user_prompt.model_id.region, thread_sensitive=True)()

                loop = asyncio.get_event_loop()
                future = ensure_future(streaming_chat_feishu(
                    system_prompt=user_prompt.system_prompt,
                    messages=messages,
                    model_id=model_id,
                    model_region=model_region,
                    max_tokens=user_prompt.max_tokens,
                    stop_sequences=user_prompt.stop_sequences,
                    temperature=user_prompt.temperature,
                    sender=sender,
                    user_id=user_id,
                ))
        return JsonResponse({'message': 'ok'})



         
                