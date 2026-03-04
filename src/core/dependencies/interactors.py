from dishka import Provider, provide, Scope

from app.interactors.product.get_product import GetProductByIdInteractor
from app.interactors.product.delete_product import DeleteProductInteractor
from app.interactors.category.create_category import CreateCategoryInteractor
from app.interactors.product.create_product import CreateProductInteractor
from app.interactors.cart.add_item_to_cart import AddItemToCartInetractor
from app.interactors.cart.get_cart import GetOrCreateCartInteractor
from app.interactors.user.create_user import CreateUserInteractor


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    # USER
    create_user = provide(CreateUserInteractor)
    get_user_cart = provide(GetOrCreateCartInteractor)
    add_item_to_cart = provide(AddItemToCartInetractor)

    # PRODUCT
    create_product = provide(CreateProductInteractor)
    delete_product = provide(DeleteProductInteractor)
    get_product_by_id = provide(GetProductByIdInteractor)

    # CATEGORY
    create_category = provide(CreateCategoryInteractor)
