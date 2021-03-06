import pytest

from contextlib_ext import suppress, async_suppress, asynccontextmanager


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


@pytest.fixture
def testmanager():
    @asynccontextmanager
    async def _testmanager(l):
        l[0] = 'entered'
        try:
            yield
        except Exception:
            l[0] = 'excepted'
            raise
        else:
            l[0] = 'exited'
    return _testmanager


async def test_asynccontextmanager(testmanager):
    var = ['']
    manager = testmanager(var)
    assert var[0] == ''
    async with manager:
        assert var[0] == 'entered'
    assert var[0] == 'exited'


async def test_asynccontextmanager_exception(testmanager):
    var = ['']
    manager = testmanager(var)
    assert var[0] == ''
    with pytest.raises(ValueError):
        async with manager:
            assert var[0] == 'entered'
            raise ValueError
    assert var[0] == 'excepted'


async def test_asynccontextmanager_as_decorator(testmanager):
    var = ['']
    @testmanager(var)
    async def func():
        assert var[0] == 'entered'
    assert var[0] == ''
    await func()
    assert var[0] == 'exited'


async def test_asynccontextmanager_as_decorator_exception(testmanager):
    var = ['']
    @testmanager(var)
    async def func():
        assert var[0] == 'entered'
        raise ValueError
    assert var[0] == ''
    with pytest.raises(ValueError):
        await func()
    assert var[0] == 'excepted'
