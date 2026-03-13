from dishka import Provider, provide, Scope

from app.interactors.cart.update_cart_item import UpdateCartItemInteractor
from app.interactors.product.get_product import GetProductByIdInteractor
from app.interactors.product.delete_product import DeleteProductInteractor
from app.interactors.category.create_category import CreateCategoryInteractor
from app.interactors.product.create_product import CreateProductInteractor
from app.interactors.cart.add_item_to_cart import AddItemToCartInetractor
from app.interactors.cart.get_cart import GetCartInteractor
from app.interactors.product.get_products import GetProductListInteractor
from app.interactors.user.create_user import CreateUserInteractor


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    # USER
    create_user = provide(CreateUserInteractor)
    get_user_cart = provide(GetCartInteractor)
    add_item_to_cart = provide(AddItemToCartInetractor)

    # CART
    update_cart_item_quantity = provide(UpdateCartItemInteractor)

    # PRODUCT
    create_product = provide(CreateProductInteractor)
    delete_product = provide(DeleteProductInteractor)
    get_product_by_id = provide(GetProductByIdInteractor)
    get_product_list = provide(GetProductListInteractor)

    # CATEGORY
    create_category = provide(CreateCategoryInteractor)
