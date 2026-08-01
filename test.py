import time
from functionalthreading import Thread, partial, _, always, thunkify, chain, tap, tmap, tforeach, tfilter, reduce

def test_Thread():
    assert Thread.__doc__, 'Should have docs.'

    def f(n):
        return n ** 2

    t = Thread(name='test', daemon=True, target=f, args=[3])
    t.start()
    t.join()
    assert t.result == 9, f't.result ({t.result}) != 9'
    assert t.name == 'test', f't.name ({t.name}) != \'test\''
    assert t.daemon == True, f't.daemon ({t.daemon}) != True'

    def f(a, b, c):
        return a + b + c

    t = Thread(target=f, args=[1, 2, 3])
    t.start()
    t.join()
    assert t.result == 6, f't.result ({t.result}) != 6'

    t = Thread(target=f, kwargs={ 'a': 1, 'b': 2, 'c': 3 })
    t.start()
    t.join()
    assert t.result == 6, f't.result ({t.result}) != 6'

def test_partial_and__():
    assert partial.__doc__, 'Should have docs.'

    def f(a, b, c):
        return a + b + c

    g = partial(f, 1)
    h = partial(g, 2)
    ret = h(3)

    def f(a, b, c):
        return [a, b, c]

    g = partial(f, _, _, 3)
    h = partial(g, 1)
    ret = h(2)

    assert ret[0] == 1, f'ret[0] ({ret[0]}) != 1'
    assert ret[1] == 2, f'ret[1] ({ret[1]}) != 2'
    assert ret[2] == 3, f'ret[2] ({ret[2]}) != 3'

def test_always():
    assert always.__doc__, 'Should have docs.'

    always1 = always(1)
    ret = always1()
    assert ret == 1, f'ret ({ret}) != 1'
    ret = always1()
    assert ret == 1, f'ret ({ret}) != 1'
    ret = always1()
    assert ret == 1, f'ret ({ret}) != 1'

def test_thunkify():
    assert thunkify.__doc__, 'Should have docs.'

    def add(a, b, c):
        return a + b + c

    thunkAdd123 = thunkify(add, 1, 2, 3)
    ret = thunkAdd123()
    assert ret == 6, f'ret ({ret}) != 6'
    ret = thunkAdd123()
    assert ret == 6, f'ret ({ret}) != 6'
    ret = thunkAdd123()
    assert ret == 6, f'ret ({ret}) != 6'

    thunkAdd123 = thunkify(add, 1, b=2, c=3)
    ret = thunkAdd123()
    assert ret == 6, f'ret ({ret}) != 6'
    ret = thunkAdd123()
    assert ret == 6, f'ret ({ret}) != 6'
    ret = thunkAdd123()
    assert ret == 6, f'ret ({ret}) != 6'

def test_chain():
    assert chain.__doc__, 'Should have docs.'

    ret = chain(
        1,
        lambda n: n + 1,
        lambda n: n ** 2,
        lambda n: n * 3,
    )
    assert ret == 12, f'({ret}) != 12'

    func_chain = chain(
        lambda n: n + 1,
        lambda n: n ** 2,
        lambda n: n * 3,
    )
    ret = func_chain(1)
    assert ret == 12, '12'

def test_tap():
    assert tap.__doc__, 'Should have docs.'

    ret = tap(lambda n: n + 1)(1)
    assert ret == 1, f'({ret}) != 1'

    n = None
    def f(_n):
        nonlocal n
        n = _n

    ret = tap(f)(1)
    assert ret == 1, f'ret ({ret}) != 1'
    assert n == 1, f'n ({n}) != 1'

def test_tmap():
    assert tmap.__doc__, 'Should have docs.'

    ret = tmap([1, 2, 3], lambda n: n ** 2)
    assert ret[0] == 1, f'ret[0] ({ret[0]}) != 1'
    assert ret[1] == 4, f'ret[1] ({ret[1]}) != 4'
    assert ret[2] == 9, f'ret[2] ({ret[2]}) != 9'

    mapping_func = tmap(lambda n: n ** 2)
    ret = mapping_func([1, 2, 3])
    assert ret[0] == 1, f'ret[0] ({ret[0]}) != 1'
    assert ret[1] == 4, f'ret[1] ({ret[1]}) != 4'
    assert ret[2] == 9, f'ret[2] ({ret[2]}) != 9'

    def f(n):
        time.sleep(1)
        return n + 1

    start = time.time()
    ret = tmap([1, 2, 3], f)
    end = time.time()

    assert ret[0] == 2, f'ret[0] ({ret[0]}) != 2'
    assert ret[1] == 3, f'ret[1] ({ret[1]}) != 3'
    assert ret[2] == 4, f'ret[2] ({ret[2]}) != 4'
    assert end - start < 1.1, 'Took too much time.'

def test_tforeach():
    assert tforeach.__doc__, 'Should have docs.'

    numbers = []
    def f(n):
        nonlocal numbers
        numbers.append(n)

    ret = tforeach([1, 2, 3], f)

    assert ret == None, f'ret ({ret}) != None'
    assert numbers[0] == 1, f'ret[0] ({ret[0]}) != 1'
    assert numbers[1] == 2, f'ret[1] ({ret[1]}) != 2'
    assert numbers[2] == 3, f'ret[2] ({ret[2]}) != 3'

    foreach_func = tforeach(f)
    ret = foreach_func([1, 2, 3])

    assert ret == None, f'ret ({ret}) != None'
    assert numbers[0] == 1, f'ret[0] ({ret[0]}) != 1'
    assert numbers[1] == 2, f'ret[1] ({ret[1]}) != 2'
    assert numbers[2] == 3, f'ret[2] ({ret[2]}) != 3'

def test_tfilter():
    assert tfilter.__doc__, 'Should have docs.'

    def is_odd(n):
        return n % 2 == 1

    ret = tfilter([1, 2, 3, 4, 5], is_odd)
    assert len(ret) == 3, f'len(ret) ({len(ret)}) != 3'
    assert ret[0] == 1, f'ret[0] ({ret[0]}) != 1'
    assert ret[1] == 3, f'ret[1] ({ret[1]}) != 3'
    assert ret[2] == 5, f'ret[2] ({ret[2]}) != 5'

    filter_odds = tfilter(is_odd)
    ret = filter_odds([1, 2, 3, 4, 5])
    assert len(ret) == 3, f'len(ret) ({len(ret)}) != 3'
    assert ret[0] == 1, f'ret[0] ({ret[0]}) != 1'
    assert ret[1] == 3, f'ret[1] ({ret[1]}) != 3'
    assert ret[2] == 5, f'ret[2] ({ret[2]}) != 5'

def test_reduce():
    assert reduce.__doc__, 'Should have docs.'

    def add(a, b):
        return a + b

    ret = reduce([1, 2, 3, 4, 5], add)
    assert ret == 15, f'ret ({ret}) != 15'

    ret = reduce([1, 2, 3, 4, 5], add, 10)
    assert ret == 25, f'ret ({ret}) != 25'

    reducing_func = reduce(add)
    ret = reducing_func([1, 2, 3, 4, 5])
    assert ret == 15, f'ret ({ret}) != 15'

    reducing_func = reduce(add, 10)
    ret = reducing_func([1, 2, 3, 4, 5])
    assert ret == 25, f'ret ({ret}) != 25'

def test():
    test_Thread()
    test_partial_and__()
    test_always()
    test_thunkify()
    test_chain()
    test_tap()
    test_tmap()
    test_tforeach()
    test_tfilter()
    test_reduce()

if __name__ == '__main__':
    test()
