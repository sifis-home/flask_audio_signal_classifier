# from unittest.mock import patch


# from app import on_close, on_error, on_open


# def test_on_error():
#     error = "WebSocket error occurred"

#     with patch("builtins.print") as mock_print:
#         on_error(None, error)

#     mock_print.assert_called_once_with(error)


# def test_on_close():
#     close_status_code = 1000
#     close_msg = "Connection closed"

#     with patch("builtins.print") as mock_print:
#         on_close(None, close_status_code, close_msg)

#     mock_print.assert_called_once_with("### Connection closed ###")


# def test_on_open():
#     with patch("builtins.print") as mock_print:
#         on_open(None)

#     mock_print.assert_called_once_with("### Connection established ###")
