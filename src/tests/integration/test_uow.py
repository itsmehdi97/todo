import pytest

from domain import model


@pytest.mark.asyncio
async def test_uow_can_commit_trx(uow):
    async with uow:
        prop = model.Prop(id=5, price=123, owner=1)
        await uow.props.add(prop)

        offer = model.Offer(price=200, user_id=2)
        offer.prop = prop
        await uow.offers.add(offer)
        await uow.commit()

    async with uow:
        p1 = await uow.props.get_by_id(5)
        o1 = await uow.offers.get_by_id(1)
        assert p1 and p1.id == 5
        assert o1 and o1.id == 1


@pytest.mark.asyncio
async def test_uow_rolls_back_uncommited_trx(uow):
    async with uow:
        prop = model.Prop(id=5, price=123, owner=1)
        await uow.props.add(prop)

    async with uow:
        p1 = await uow.props.get_by_id(5)
        assert p1 is None
