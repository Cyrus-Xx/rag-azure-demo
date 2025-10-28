# test_main.py
def test_app_imports():
    """Verify that main.py can be imported without errors (e.g., missing PDF, invalid key)."""
    import main
    assert main is not None