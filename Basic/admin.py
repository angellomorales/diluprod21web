from django.contrib import admin

from .models import Campo, Pozo, DataAVM, DataStork, DataAgar


class CampoAdmin(admin.ModelAdmin):
    filter_horizontal = ("pozos",)


admin.site.register(Campo, CampoAdmin)
admin.site.register(Pozo)
admin.site.register(DataAVM)
admin.site.register(DataStork)
admin.site.register(DataAgar)
