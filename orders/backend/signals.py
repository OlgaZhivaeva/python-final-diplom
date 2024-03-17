from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver, Signal
from django_rest_passwordreset.signals import reset_password_token_created


from backend.models import ConfirmEmailToken, User

new_user_registered = Signal()

new_order = Signal()

edit_order_state = Signal()

export_order = Signal()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param kwargs:
    :return:
    """
    # send an e-mail to the user

    msg = EmailMultiAlternatives(
        # title:
        f'Password Reset Token for {reset_password_token.user}',
        # message:
        reset_password_token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    msg.send()


@receiver(new_user_registered)
def new_user_registered_signal(user_id, **kwargs):
    """
    отправляем письмо с подтверждением почты
    """
    # send an e-mail to the user
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f'Password Reset Token for {token.user.email}',
        # message:
        token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [token.user.email]
    )
    msg.send()
    print(f'Письмо отправлено {token.user.email}')


@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    """
    отправляем письмо при отправке заказа покупателем
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        'Спасибо за заказ',
        # message:
        'Заказ сформирован',
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email]
    )
    msg.send()
    print(f'Заказ сформирован {user.email}')

@receiver(edit_order_state)
def edit_order_state_signal(user_id, state, **kwargs):
    """
    отправляем письмо при редактировании статуса заказа администратором
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)
    dict_choices = {
        'assembled': 'собран',
        'sent': 'отправлен',
        'delivered': 'доставлен',
        'canceled': 'отменен'
    }

    msg = EmailMultiAlternatives(
        # title:
        f"Обновление статуса заказа",
        # message:
        f'Заказ {dict_choices[state]}',
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email]
    )
    msg.send()
    print(f'Статус заказа изменен {dict_choices[state]} {user.email} {user}')


@receiver(export_order)
def export_order_signal(user_id, order_id, **kwargs):
    """
    Экспорт заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)
    msg = EmailMultiAlternatives(
        # title:
        'Заказ подтвержден',
        # message:
        f'Заказ {order_id} подтвержден',
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email]
    )
    msg.send()

    print(f'Экспорт заказа {order_id}')
