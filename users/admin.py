from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Person, Relation, XtraPhotos, XtraInfo

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = ['id', 'first_name', 'last_name', 'city', 'profession', 'birth_date']
    search_fields = ['first_name', 'last_name', ]
    list_filter = ('last_name',)
    readonly_fields = ['created_at', 'updated_at']
    #fields = ['first_name', 'last_name', ('birth_date', 'date_of_death')]
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', ('birth_date', 'date_of_death'), 'city', 'profession', 'thumbnail')
        }),
        ('Position', {
            'fields': ('x_pos', 'y_pos')
        }),
        ('Other', {
            'fields': ('phone_number', 'cell_number', 'email')
        }),
    )


    def get_name(self, obj):
        return obj.last_name.name
    get_name.admin_order_field = 'last_name'


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    model = Relation
    list_display = ['id', 'parent', 'child']
    ordering = ['parent__first_name']
    search_fields = ('parent__first_name', 'parent__last_name',
                     'child__first_name', 'child__last_name')
    raw_id_fields = ('parent','child')

    """ def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Relation.objects.filter(
                parent__in=['Hirt', 'Schwab'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
     """

@admin.register(XtraPhotos)
class XtraPhotosAdmin(admin.ModelAdmin):
    model = XtraPhotos
    raw_id_fields = ('parent',)
    list_display = ['id', 'parent', 'title', 'caption', 'source', 'created_at']


@admin.register(XtraInfo)
class XtraInfoAdmin(admin.ModelAdmin):
    model = XtraInfo
    raw_id_fields = ('parent',)
    list_display = ['id', 'parent', 'title', 'created_at']

admin.site.register(CustomUser, CustomUserAdmin)
#admin.site.register(Person, PersonAdmin)
# admin.site.register(Relation, RelationAdmin)
