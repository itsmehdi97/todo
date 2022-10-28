import asyncio
import pytest
from datetime import timedelta, datetime

from sqlalchemy import select

from fastapi.testclient import TestClient
from jose import jwt

from domain import model
from api.server import get_application
from core.config import get_settings


settings = get_settings()


@pytest.fixture
def test_client():
    with TestClient(get_application()) as client:
        yield client


@pytest.fixture
def auth_token():
    to_encode = {"sub": "tesetuser", "uid": 1}
    expire = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": datetime.utcnow() + expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@pytest.mark.asyncio
async def test_place_offer(test_client, auth_token, db):
    db.add(model.Prop(price=10, owner=2, id=5, created_at=datetime.now()))
    await db.commit()

    resp = test_client.post(
        "/api/offers/place",
        json={"prop_id": 5, "price": 110},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200
    
    first_offer = (await db.execute(select(model.Offer).where(model.Offer.id == 1))).scalar()
    assert first_offer.status == model.OfferStatus.PENDING

    resp = test_client.post(
        "/api/offers/place",
        json={"prop_id": 5, "price": 300},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200
    await db.refresh(first_offer)
    assert first_offer.status == model.OfferStatus.RAISED

    second_offer = (await db.execute(select(model.Offer).where(model.Offer.id == 2))).scalar()
    assert second_offer.status == model.OfferStatus.PENDING

    await asyncio.sleep(settings.ACCEPT_DELAY_SECONDS + 5)  # wait for accept
    print("# slept", int(settings.ACCEPT_DELAY_SECONDS) + 5)

    await db.refresh(second_offer)
    assert second_offer.status == model.OfferStatus.ACCEPTED

@pytest.mark.asyncio
async def test_place_offer_low_price(test_client, auth_token, db):
    db.add(model.Prop(price=10, owner=2, id=5, created_at=datetime.now()))
    await db.commit()

    resp = test_client.post(
        "/api/offers/place",
        json={"prop_id": 5, "price": 5},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_offer_on_nonexisting_prop(test_client, auth_token, db):
    resp = test_client.post(
        "/api/offers/place",
        json={"prop_id": 5, "price": 5},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert resp.status_code == 400



