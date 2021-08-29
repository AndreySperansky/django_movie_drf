from django import forms
from django.contrib import admin
from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Review

from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from modeltranslation.admin import TranslationAdmin


# class CategoryAdmin(admin.ModelAdmin):
#     """Категории"""
#     list_display = ( "id", "name", "url",)
#     list_display_links = ("name",)


# admin.site.register(Category, CategoryAdmin)      # в случае регистрации через декоратор можно удалить
# admin.site.register(Movie)                        # в случае регистрации через декоратор можно удалить
# admin.site.register(MovieShots)                   # в случае регистрации через декоратор можно удалить
# admin.site.register(Actor)                        # в случае регистрации через декоратор можно удалить


class MovieAdminForm(forms.ModelForm):
    """Форма с виджетом ckeditor"""
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    # description_en = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "url", )
    list_display_links = ("name",)



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы к фильму"""
    list_display = ("id", "name", "email", "parent", "movie",)
    readonly_fields = ("name", "email")


class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Review
    extra = 1
    readonly_fields = ("name", "email")


'''
Кадры из фильма в админке
'''

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"




'''
Кадры из фильма горизонтально для передачи в админку "MovieAdmin"
stackedInline - отображение вертикально
TabularInline - отображение горизонтально
'''

class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Изображение"





@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInline, ReviewInline]
    # Вводим класс MovieShotsInline (отображение кадра)  к фильму в админке
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ["publish", "unpublish"]
    form = MovieAdminForm
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }),
        # Для отображения "poster", "get_image" в одной строке помещфем их в картеж

        (None, {
            "fields": (("year", "world_premiere", "country"),)
            
        }),
        
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
            
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fess_in_world"),)
            
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

################################################################################
#                           ACTIONS
################################################################################

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")


    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)


    get_image.short_description = "Постер"
#   Изменение отображение поля get_image на Постер


#####################################################################
#                      ЖАНРЫ
#####################################################################



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")




'''***************************************************
АКТЕРЫ И РЕЖИССЕРЫ
******************************************************'''

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):

    """Актеры"""
    list_display = ("name", "age", "image",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50"')
        # mark_safe выводит html не как строку а как тег

    get_image.short_description = "Изображение"



'''
РЕЙТИНГ
'''

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "movie", "ip")


admin.site.register(RatingStar)




admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"

# ДЛя замены стандартного заголовка админки "Администрирование Django"
# на Django Movies
