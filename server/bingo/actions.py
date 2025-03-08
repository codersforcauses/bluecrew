from django.http import HttpResponse
from django.contrib.admin import action
from .models import User, TileInteraction


def get_friendly_value(instance, field_name, value):
    display_method = f'get_{field_name}_display'
    if hasattr(instance, display_method):
        return getattr(instance, display_method)()
    else:
        # If it's not a choice field, return the raw value
        return value


@action(description="Export selected objects as CSV")
def export2csv(modeladmin, request, queryset):
    import csv

    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{modeladmin.model._meta.model_name}s.csv"'},
    )

    writer = csv.writer(response)
    if modeladmin.model == User:
        exclude = ('password', 'is_superuser', 'is_active')
    elif modeladmin.model == TileInteraction:
        exclude = ('image_display',)
    else:
        exclude = tuple()

    fields = modeladmin.fields if modeladmin.fields else [
        f.name for f in modeladmin.model._meta.fields()]
    fields = [f for f in fields if f not in exclude]
    writer.writerow(fields)
    if modeladmin.model == User:
        queryset = queryset.filter(is_superuser=False, is_active=True)
    raw_values = queryset.values_list(*fields)
    readable_rows = []
    for instance, values in zip(queryset, raw_values):
        readable_rows.append((get_friendly_value(instance, field_name, value)
                             for field_name, value in zip(fields, values)))

    writer.writerows(readable_rows)
    return response
