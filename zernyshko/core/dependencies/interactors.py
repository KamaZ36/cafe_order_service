from dishka import Provider, Scope, provide

from zernyshko.app.interactors.cart.add_item_to_cart import AddItemToCartInetractor
from zernyshko.app.interactors.cart.get_cart import GetCartInteractor
from zernyshko.app.interactors.cart.update_cart_item import UpdateCartItemInteractor
from zernyshko.app.interactors.category.create_category import CreateCategoryInteractor
from zernyshko.app.interactors.category.delete_category import DeleteCategoryInteractor
from zernyshko.app.interactors.category.get_categories import GetCategoryListInteractor
from zernyshko.app.interactors.category.update_category import UpdateCategoryInteractor
from zernyshko.app.interactors.order.cancel import StaffCancelOrderInteractor
from zernyshko.app.interactors.order.complete import CompleteOrderInteractor
from zernyshko.app.interactors.order.confirm import ConfirmOrderInteractor
from zernyshko.app.interactors.order.create import CreateOrderInteractor
from zernyshko.app.interactors.order.get_orders import GetStaffOrderListInteractor
from zernyshko.app.interactors.order.mark_ready import MarkOrderReadyInteractor
from zernyshko.app.interactors.order.simulate_payment import (
    SimulateOrderPaymentInteractor,
)
from zernyshko.app.interactors.payment.handle_webhook import (
    HandlePaymentWebhookInteractor,
)
from zernyshko.app.interactors.product.create_product import CreateProductInteractor
from zernyshko.app.interactors.product.delete_product import DeleteProductInteractor
from zernyshko.app.interactors.product.get_product import GetProductByIdInteractor
from zernyshko.app.interactors.product.get_products import GetProductListInteractor
from zernyshko.app.interactors.product.update_product import UpdateProductInteractor
from zernyshko.app.interactors.user.cancel_order import CancelOrderInteractor
from zernyshko.app.interactors.user.create_user import CreateUserInteractor
from zernyshko.app.interactors.user.get_current_user import GetCurrentUserInteractor
from zernyshko.app.interactors.user.get_orders import GetOrderListInteractor
from zernyshko.app.interactors.user.get_staff_user_detail import (
    GetStaffUserDetailInteractor,
)
from zernyshko.app.interactors.user.get_staff_user_list import GetStaffUserListInteractor
from zernyshko.app.interactors.user.get_staff_user_payments import (
    GetStaffUserPaymentsInteractor,
)
from zernyshko.app.interactors.user.login import LoginInteractor
from zernyshko.app.interactors.user.logout import LogoutInteractor
from zernyshko.app.interactors.user.provision_staff import ProvisionStaffInteractor
from zernyshko.app.interactors.user.resolve_phone_user import ResolvePhoneUserInteractor
from zernyshko.app.interactors.user.send_phone_code import (
    SendPhoneVerificationCodeInteractor,
)
from zernyshko.app.interactors.user.verify_phone_code import VerifyPhoneCodeInteractor


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    # USER
    create_user = provide(CreateUserInteractor)
    resolve_phone_user = provide(ResolvePhoneUserInteractor)
    send_phone_verification_code = provide(SendPhoneVerificationCodeInteractor)
    verify_phone_code = provide(VerifyPhoneCodeInteractor)
    login = provide(LoginInteractor)
    logout = provide(LogoutInteractor)
    get_current_user = provide(GetCurrentUserInteractor)
    provision_staff = provide(ProvisionStaffInteractor)
    get_user_cart = provide(GetCartInteractor)
    add_item_to_cart = provide(AddItemToCartInetractor)
    get_order_list = provide(GetOrderListInteractor)
    cancel_order = provide(CancelOrderInteractor)
    get_staff_user_list = provide(GetStaffUserListInteractor)
    get_staff_user_detail = provide(GetStaffUserDetailInteractor)
    get_staff_user_payments = provide(GetStaffUserPaymentsInteractor)

    # CART
    update_cart_item_quantity = provide(UpdateCartItemInteractor)

    # PRODUCT
    create_product = provide(CreateProductInteractor)
    update_product = provide(UpdateProductInteractor)
    delete_product = provide(DeleteProductInteractor)
    get_product_by_id = provide(GetProductByIdInteractor)
    get_product_list = provide(GetProductListInteractor)

    # CATEGORY
    create_category = provide(CreateCategoryInteractor)
    get_category_list = provide(GetCategoryListInteractor)
    update_category = provide(UpdateCategoryInteractor)
    delete_category = provide(DeleteCategoryInteractor)

    # ORDER
    create_order = provide(CreateOrderInteractor)
    get_staff_order_list = provide(GetStaffOrderListInteractor)
    staff_cancel_order = provide(StaffCancelOrderInteractor)
    confirm_order = provide(ConfirmOrderInteractor)
    mark_order_ready = provide(MarkOrderReadyInteractor)
    complete_order = provide(CompleteOrderInteractor)
    simulate_order_payment = provide(SimulateOrderPaymentInteractor)

    # PAYMENT
    handle_payment_webhook = provide(HandlePaymentWebhookInteractor)
