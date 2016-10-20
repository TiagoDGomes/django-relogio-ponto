from django.contrib import admin
from core.models import RelogioPonto, Colaborador, Parametro

class ParametroInline(admin.StackedInline):
    model = Parametro
    extra = 0
    max_num = 0

@admin.register(RelogioPonto)
class RelogioPontoAdmin(admin.ModelAdmin):
    inlines = [ParametroInline,]
    
    def get_inline_instances(self, request, obj=None):
        if obj:
            return [inline(self.model, self.admin_site) for inline in self.inlines]
        else:
            return []
        
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if not object_id:
            extra_context['show_save'] = False
        
        return super(RelogioPontoAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)
        
@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    pass
