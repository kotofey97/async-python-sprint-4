from http import HTTPStatus

import pytest
from fastapi import status
from httpx import AsyncClient

from core.config import app_settings
from main import app


@pytest.mark.asyncio()
async def test_get_db_status(client: AsyncClient):
    response = await client.get('/api/v1/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'version': 'v1'}


@pytest.mark.asyncio()
async def test_ping(client: AsyncClient) -> None:
    response = await client.get('/api/v1/ping')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {'connection_db': True}


@pytest.mark.asyncio()
async def test_create_short_url(client: AsyncClient, test_urls) -> None:
    response = await client.post(
        app.url_path_for("create_short_url"),
        json={'original_url': test_urls[0]}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert 'short_url' in data.keys()
    assert 'url_id' in data.keys()
    assert len(data['url_id']) == 8


@pytest.mark.asyncio()
async def test_create_and_get_short_urls(client: AsyncClient, test_urls) -> None:
    response = await client.post(
        app.url_path_for("create_short_urls"),
        json=[{'original_url': url} for url in test_urls]
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert len(data) == 3
    url_in_db = data[0]['url_id']
    response = await client.get(app.url_path_for(
        "get_url",
        url_id=url_in_db)
    )
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers.get('Location') == test_urls[0]


@pytest.mark.asyncio()
async def test_get_url_status(client: AsyncClient, test_urls) -> None:
    response = await client.post(
        app.url_path_for("create_short_url"),
        json={'original_url': test_urls[0]}
    )
    assert response.status_code == status.HTTP_201_CREATED
    
    short_url = response.json()['url_id']

    response = await client.get(app.url_path_for(
        "get_url",
        url_id=short_url)
    )
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

    response = await client.get(
        app.url_path_for("get_url_status", url_id=short_url),
        params={'full-info': False},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["usages_count"] == 1

    response = await client.get(
        app.url_path_for("get_url_status", url_id=short_url),
        params={'full-info': True},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    for field in ['short_url', 'id', 'client', 'use_at']:
        assert field in data[0].keys()
