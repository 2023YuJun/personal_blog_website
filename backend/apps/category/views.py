from rest_framework.views import APIView
from rest_framework import status
from apps.category.service import *
from utils.result import result, ERRORCODE, throw_error

error_code = ERRORCODE['CATEGORY']


class CategoryView(APIView):
    """
    分类控制器
    """

    def post(self, request, *args, **kwargs):
        if 'add' in request.path:
            return self.add_category(request)
        elif 'delete' in request.path:
            return self.delete_categories(request)
        elif 'getCategoryList' in request.path:
            return self.get_category_list(request)

    def put(self, request, *args, **kwargs):
        if 'update' in request.path:
            return self.update_category(request)

    def get(self, request, *args, **kwargs):
        if 'getCategoryDictionary' in request.path:
            return self.get_category_dictionary(request)

    def add_category(self, request):
        try:
            category = request.data
            response = verify_category(category)
            if response is None:
                res = create_category(category)
                return Response(result("新增分类成功", {
                    "id": res.id,
                    "category_name": res.category_name,
                }), status=status.HTTP_201_CREATED)
            else:
                return response
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "新增分类失败"), status=500)

    def update_category(self, request):
        try:
            category = request.data
            response = verify_category(category)
            if response is None:
                res = update_category(category)
                return Response(result("修改分类成功", res), status=status.HTTP_200_OK)
            else:
                return response
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "修改分类失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_categories(self, request):
        try:
            category = request.data
            response = verify_delete_categories(category)
            if response is None:
                res = delete_categories(category)
                return Response(result("删除分类成功", {
                    "updateNum": res,
                }), status=status.HTTP_200_OK)
            else:
                return response
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "删除分类失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_category_list(self, request):
        try:
            category = request.data
            res = get_category_list(category)
            return Response(result("分页查找分类成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "分页查找分类失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_category_dictionary(self, request):
        try:
            res = get_category_dictionary()
            return Response(result("获取分类字典成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取分类字典失败"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
