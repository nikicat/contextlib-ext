import pytest

from contextlib_ext import suppress, async_suppress


class SuppressedException(Exception):
    pass


class PassedException(Exception):
    pass


def test_suppress_contextmanager_silent():
    with suppress(SuppressedException):
        raise SuppressedException


def test_suppress_contextmanager_rising():
    with pytest.raises(PassedException):
        with suppress(SuppressedException):
            raise PassedException


def test_suppress_decorator_silent():
    @suppress(SuppressedException)
    def silent():
        raise SuppressedException

    silent()
    silent()


def test_suppress_decorator_raising():
    @suppress(SuppressedException)
    def raising():
        raise PassedException

    with pytest.raises(PassedException):
        raising()
    with pytest.raises(PassedException):
        raising()


async def test_async_suppress_contextmanager_silent():
    async with async_suppress(SuppressedException):
        raise SuppressedException


async def test_async_suppress_contextmanager_raising():
    with pytest.raises(PassedException):
        async with async_suppress(SuppressedException):
            raise PassedException


async def test_async_suppress_decorator_silent():
    @async_suppress(SuppressedException)
    async def silent():
        raise SuppressedException

    await silent()
    await silent()


async def test_async_suppress_decorator_raising():
    @async_suppress(SuppressedException)
    async def raising():
        raise PassedException

    with pytest.raises(PassedException):
        await raising()
    with pytest.raises(PassedException):
        await raising()
