from django.contrib import admin

from .models import Campo, Pozo, DataAVM, DataStork, PozoInyector


class CampoAdmin(admin.ModelAdmin):
    filter_horizontal = ("pozos",)

class PozoInyectorAdmin(admin.ModelAdmin):
    filter_horizontal = ("pozosAsociados",)


admin.site.register(Campo, CampoAdmin)
admin.site.register(Pozo)
admin.site.register(DataAVM)
admin.site.register(DataStork)
admin.site.register(PozoInyector,PozoInyectorAdmin)
