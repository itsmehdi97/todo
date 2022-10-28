from unittest.mock import Mock
import pytest

from core.config import Settings
from domain import model
from domain.model import OfferStatus
from domain import exceptions as exc


settings = Settings()
PRICE_TRESHOLD = settings.OFFER_PRICE_TRESHOLD
ACCEPT_DELAY_SECONDS = settings.ACCEPT_DELAY_SECONDS


def test_price_equal_valid_price_offer():
    max_price_offer = 100
    offer = model.Offer(price=max_price_offer+PRICE_TRESHOLD, user_id=1)
    assert offer._is_valid_price(max_price_offer) is True


def test_price_gt_valid_price_offer():
    max_price_offer = 100
    offer = model.Offer(price=max_price_offer+PRICE_TRESHOLD + 10, user_id=1)
    assert offer._is_valid_price(max_price_offer) is True


def test_price_lt_vaild_price_offer():
    max_price_offer = 100
    offer = model.Offer(price=max_price_offer+PRICE_TRESHOLD - 10, user_id=1)
    assert offer._is_valid_price(max_price_offer) is False


def test_place_offer_with_invalid_price(prop: model.Prop):
    offer = model.Offer(price=prop.price - 10, user_id=2)
    offer._is_valid_price = Mock(return_value=False)
    
    with pytest.raises(exc.LowPriceException):
        offer.place(prop)


def test_cant_place_offer_on_owning_prop(prop: model.Prop):
    offer = model.Offer(price=prop.max_offer_price + PRICE_TRESHOLD, user_id=1)
    offer._is_valid_price = Mock(return_value=True)

    assert prop.owner == offer.user_id  # sanity check
    with pytest.raises(exc.OperationNotPermittedException):
        offer.place(prop)


def test_pending_offer_left_unchange_for_invalid_offer_placement(prop: model.Prop):
    old_offer = model.Offer(price=prop.max_offer_price + PRICE_TRESHOLD, user_id=2)
    old_offer._is_valid_price = Mock(return_value=True)
    old_offer.place(prop)
    assert prop.pending_offer == old_offer  # sanity check

    failing_offer = model.Offer(price=0, user_id=2)
    failing_offer._is_valid_price = Mock(return_value=False)

    with pytest.raises(exc.LowPriceException):
        failing_offer.place(prop)

    assert prop.pending_offer == old_offer


def test_pending_offer_updated_for_valid_offer(prop: model.Prop):
    old_offer = model.Offer(price=prop.max_offer_price + PRICE_TRESHOLD, user_id=2)
    old_offer._is_valid_price = Mock(return_value=True)
    old_offer.place(prop)
    assert prop.pending_offer == old_offer  # sanity check

    offer = model.Offer(price=prop.max_offer_price + PRICE_TRESHOLD, user_id=2)
    offer._is_valid_price = Mock(return_value=True)
    offer.place(prop)

    assert prop.pending_offer == offer
    assert old_offer.status == OfferStatus.RAISED


def test_accept_nonpending_offer():
    offer = model.Offer(price=0, user_id=2, status=OfferStatus.RAISED)
    with pytest.raises(exc.OperationNotPermittedException):
        offer.accept()
