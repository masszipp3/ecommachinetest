from shop_admin.models import Categories
def get_category_list(self):
    category_list = Categories.objects.all()
    return {'category_list' : category_list}