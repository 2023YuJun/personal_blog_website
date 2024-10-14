from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from apps.chat.service import *
from utils.result import result, ERRORCODE, throw_error
from utils.minioUpload import delete_minio_imgs

error_code = ERRORCODE['CHAT']


class ChatView(APIView):
    """
    聊天控制器
    """

    def post(self, request, *args, **kwargs):
        if 'add' in request.path:
            return self.create_chat(request)
        elif 'delete' in request.path:
            return self.delete_chats(request)
        elif 'getChatList' in request.path:
            return self.get_chat_list(request)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if 'deleteOne' in request.path:
            return self.delete_one_chat(request, id)

    def create_chat(self, request):
        """新增聊天"""
        try:
            res = create_chat(request.data)
            return Response(result("新增聊天成功", {"content": res.content}), status=status.HTTP_201_CREATED)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "新增聊天失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_chats(self, request):
        """删除聊天"""
        try:
            arr = get_all_chats()
            if arr:
                arr = [item.content.split("/").pop() for item in arr]
                delete_minio_imgs(arr)

            res = delete_chats()
            return Response(result("删除聊天成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "删除聊天失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_one_chat(self, request, chat_id):
        """删除单条聊天记录"""
        try:
            one = get_one_chat(chat_id)
            if one.content_type == "image":
                content = one.content
                arr = [content.split("/").pop()]
                delete_minio_imgs(arr)

            res = delete_one_chat(chat_id)
            return Response(result("撤回聊天成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "撤回聊天失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_chat_list(self, request):
        """条件分页查找聊天列表"""
        try:
            res = get_chat_list(request.data)
            return Response(result("分页查找聊天成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "分页查找聊天失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
