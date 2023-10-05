from django.contrib import admin


class GuardedModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.for_user(request.user)
