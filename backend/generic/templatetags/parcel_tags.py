from django import template
from parcel_loader import get_loader

register = template.Library()

@register.simple_tag
def parcel_asset(asset_name):
    loader = get_loader("DEFAULT")
    return loader.get_asset(asset_name)
