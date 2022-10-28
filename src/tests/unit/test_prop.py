from domain import model


def test_max_offer_price(prop: model.Prop):
    assert prop.pending_offer is None

    offer1 = model.Offer(price=250, user_id=2)
    offer2 = model.Offer(price=350, user_id=2)
    offer1.place(prop)
    offer2.place(prop)
    assert prop.pending_offer == offer2
    assert prop.max_offer_price == prop.pending_offer.price


def test_max_offer_price_for_prop_without_offer(prop: model.Prop):
    assert prop.pending_offer is None
    assert prop.max_offer_price == prop.price
