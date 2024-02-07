from django.db import models
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone

class TimeSetup(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True  # Đánh dấu lớp này là một lớp trừu tượng

# Chia trang
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        res = super().get_paginated_response(data)
        res.data['page_size'] = self.page_size
        return res