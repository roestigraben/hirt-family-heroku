from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Person, Relation

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]


class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = ['id', 'first_name', 'last_name', 'city', 'profession', 'birth_date']
    search_fields = ['first_name', 'last_name', ]
    list_filter = ('last_name',)


    def get_name(self, obj):
        return obj.last_name.name
    get_name.admin_order_field = 'last_name'


class RelationAdmin(admin.ModelAdmin):
    model = Relation
    list_display = ['id', 'parent', 'child']
    ordering = ['parent__first_name']
    

    """ def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Relation.objects.filter(
                parent__in=['Hirt', 'Schwab'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
     """


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Relation, RelationAdmin)
