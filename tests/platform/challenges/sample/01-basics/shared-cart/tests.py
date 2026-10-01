def test_one_cart():
    """Одна корзина: два товара — count() == 2"""
    cart = Cart()
    cart.add("латте")
    cart.add("круассан")
    assert cart.count() == 2


def test_two_carts():
    """Товар первой корзины не попадает во вторую"""
    a, b = Cart(), Cart()
    a.add("латте")
    assert b.count() == 0, "у второй корзины появились чужие товары — список общий для всех экземпляров"


def test_new_cart_empty():
    """Новая корзина пустая, даже если раньше создавали другие"""
    Cart().add("чай")
    assert Cart().count() == 0
