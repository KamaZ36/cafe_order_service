from dishka import Provider, provide, Scope

from src.app.interactors.category.create_category import CreateCategoryInteractor
from src.app.interactors.product.create_product import CreateProductInteractor
from src.app.interactors.cart.add_item_to_cart import AddItemToCartInetractor
from src.app.interactors.cart.get_cart import GetOrCreateCartInteractor
from src.app.interactors.user.create_user import CreateUserInteractor


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    # USER
    create_user = provide(CreateUserInteractor)
    get_user_cart = provide(GetOrCreateCartInteractor)
    add_item_to_cart = provide(AddItemToCartInetractor)

    # PRODUCT
    create_product = provide(CreateProductInteractor)

    # CATEGORY
    create_category = provide(CreateCategoryInteractor)
