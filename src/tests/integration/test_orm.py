import pytest

from domain import model


@pytest.mark.asyncio
async def test_prop_pending_offer_works(uow):
    async with uow:
        prop = model.Prop(id=5, price=123, owner=1)
        await uow.props.add(prop)

        offer = model.Offer(price=200, user_id=2)
        offer.status=3
        offer2 = model.Offer(price=250, user_id=2)
        offer.prop = prop
        offer2.prop = prop
        await uow.offers.add(offer)
        await uow.offers.add(offer2)

        await uow.commit()

    async with uow:
        p1 = await uow.props.get_by_id(5)
        o1 = p1.pending_offer
        assert p1 and p1.id == 5
        assert o1 and o1.id == 2
