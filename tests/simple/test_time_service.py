from datetime import datetime
from unittest.mock import patch
from simple.time_service import is_office_open

def test_office_open():
    test_time = datetime(2025, 12, 30, 10, 0, 0)
    with patch("simple.time_service.datetime") as mock_datetime:
        mock_datetime.now.return_value = test_time
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        assert is_office_open() is True

def test_office_closed():
    test_time = datetime(2025, 12, 30, 20, 0, 0)
    with patch("simple.time_service.datetime") as mock_datetime:
        mock_datetime.now.return_value = test_time
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        assert is_office_open() is False