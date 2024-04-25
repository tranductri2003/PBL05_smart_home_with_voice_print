from django.contrib import admin
from django.forms import inlineformset_factory
from .models import Member, MemberFile
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

class LimitFileInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Kiểm tra số lượng file tải lên
        count = 0
        for form in self.forms:
            if not form.is_valid():
                continue  # Bỏ qua các form không hợp lệ
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                count += 1
        if count > 5:
            raise ValidationError("Bạn chỉ có thể tải lên tối đa 5 file.")

class MemberFileInline(admin.TabularInline):
    model = MemberFile
    formset = LimitFileInlineFormSet
    extra = 1  # Số form mặc định hiển thị là 1
    #fields = ['member', 'file', 'features']  # Thêm trường 'features' vào danh sách các trường hiển thị
    #readonly_fields = ['features']  # Đặt trường 'features' là chỉ đọc nếu bạn không muốn cho phép chỉnh sửa từ admin

class MemberAdmin(admin.ModelAdmin):
    inlines = [MemberFileInline]
    list_display = ['id', 'name', 'about']  # Hiển thị trường 'id', 'name', 'about' trong danh sách thành viên

admin.site.register(Member, MemberAdmin)
