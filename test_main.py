# test_main.py
def test_app_imports():
    import main
    assert main is not None

def test_add_function():
    from main import add
    assert add(2, 3) == 5