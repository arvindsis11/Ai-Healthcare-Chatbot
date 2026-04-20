def test_ci_ping():
    """Simple test to verify CI pipeline is working."""
    assert 1 + 1 == 2

def test_backend_environment():
    """Verify that we can import core modules."""
    try:
        import fastapi
        assert fastapi.__version__ is not None
    except ImportError:
        assert False, "fastapi not installed"
