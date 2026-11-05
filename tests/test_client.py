"""Tests of the client: a fake transport and a local HTTP server on 127.0.0.1, never the real API.

    python -m unittest discover -s tests -v
"""
import http.server
import json
import os
import socket
import sys
import threading
import time
import unittest
import urllib.parse
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

import unione  # noqa: E402
from unione.api.email import EmailSendRequest, MessageObject, MessageObjectRecipientsItem as Recipient  # noqa: E402
from unione.api.webhook import WebhookApi  # noqa: E402
from unione.client import ApiError, UrllibTransport  # noqa: E402
from unione.client.api_client import PLATFORM  # noqa: E402
from unione.common import BodyObject  # noqa: E402

API_KEY = "test-key"
BASE_URL = "http://127.0.0.1:9/api/v1"
"""Explicit base URL of the tests (a closed local port): nothing may reach the real API."""


class FakeTransport:
    """Records the requests and answers with the given (status, body) or raises the given exception."""

    def __init__(self, status=200, body=b'{"status": "success"}', error=None):
        self.status, self.body, self.error = status, body, error
        self.calls = []

    def send(self, method, url, headers, body, timeout):
        self.calls.append({"method": method, "url": url, "headers": dict(headers), "body": body, "timeout": timeout})
        if self.error is not None:
            raise self.error
        return self.status, self.body

    @property
    def last(self):
        return self.calls[-1]


def make_client(transport, api_key=API_KEY, **kwargs):
    return unione.client(api_key, BASE_URL, transport=transport, **kwargs)


def send_request():
    """The short form of email/send: a recipient from "Name <email>" and an HTML body."""
    return EmailSendRequest(message=MessageObject(
        recipients=[Recipient.from_address("User <user@example.com>")],
        body=BodyObject.from_html("<b>Hi</b>"),
        subject="Hello",
        from_email="shop@example.com",
    ))


def json_error(status, message="Unknown recipient", code=204):
    return FakeTransport(status, json.dumps({"status": "error", "message": message, "code": code}).encode())


class SendTest(unittest.TestCase):
    def test_send_request_and_response(self):
        transport = FakeTransport(200, json.dumps({
            "status": "success", "job_id": "1ZymBc-00041N-9X", "emails": ["user@example.com"],
            "failed_emails": {"bad@example.com": "unsubscribed"}}).encode())
        response = make_client(transport).email.send(send_request())

        self.assertEqual(len(transport.calls), 1)
        call = transport.last
        url = urllib.parse.urlsplit(call["url"])
        self.assertEqual(call["method"], "POST")
        self.assertEqual(url.scheme + "://" + url.netloc + url.path, BASE_URL + "/email/send.json")
        self.assertEqual(urllib.parse.parse_qs(url.query), {"platform": [PLATFORM]})
        self.assertEqual(PLATFORM, "python-sdk." + unione.__version__)
        self.assertEqual(call["headers"]["X-API-KEY"], API_KEY)
        self.assertEqual(call["headers"]["Content-Type"], "application/json")
        self.assertEqual(json.loads(call["body"].decode("utf-8")), {"message": {
            "recipients": [{"email": "user@example.com", "substitutions": {"to_name": "User"}}],
            "body": {"html": "<b>Hi</b>"},
            "subject": "Hello",
            "from_email": "shop@example.com",
        }})
        self.assertEqual(response.job_id, "1ZymBc-00041N-9X")
        self.assertEqual(response.emails, ["user@example.com"])
        self.assertEqual(response.failed_emails, {"bad@example.com": "unsubscribed"})

    def test_other_method(self):
        transport = FakeTransport(200, b'{"status": "success", "user_id": 1, "email": "user@example.com"}')
        response = make_client(transport).system.info()
        self.assertTrue(transport.last["url"].startswith(BASE_URL + "/system/info.json?"))
        self.assertEqual(json.loads(transport.last["body"].decode("utf-8")), {})
        self.assertEqual(response.user_id, 1)

    def test_platform_and_headers(self):
        transport = FakeTransport()
        make_client(transport, platform="app.1.0.0", headers={"X-Request-Id": "42"}).system.info()
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(transport.last["url"]).query)
        self.assertEqual(query, {"platform": ["app.1.0.0," + PLATFORM]})
        self.assertEqual(transport.last["headers"]["X-Request-Id"], "42")

    def test_transport_function(self):
        calls = []

        def transport(method, url, headers, body, timeout):
            calls.append(url)
            return 200, '{"status": "success"}'

        make_client(transport).system.info()
        self.assertEqual(len(calls), 1)


class ErrorTest(unittest.TestCase):
    def send(self, transport, api_key=API_KEY):
        with self.assertRaises(ApiError) as caught:
            make_client(transport, api_key).email.send(send_request())
        return caught.exception

    def test_api_error(self):
        e = self.send(json_error(400))
        self.assertEqual(e.kind, ApiError.KIND_API)
        self.assertFalse(e.retryable)
        self.assertEqual(e.error_code, 204)
        self.assertEqual(e.http_status, 400)
        self.assertEqual(e.method, "email/send")
        self.assertTrue(e.hint)
        self.assertEqual(e.api_message, "Unknown recipient")
        self.assertEqual(e.response_body["code"], 204)
        self.assertTrue(e.message.startswith("email/send: "), e.message)
        self.assertIn("(API error 204, HTTP 400)", e.message)
        self.assertIn("Fix: ", e.message)
        self.assertEqual(str(e), e.message)

    def test_retryable_statuses(self):
        for status in (429, 503):
            with self.subTest(status=status):
                e = self.send(json_error(status, "Too many requests", 2004))
                self.assertEqual(e.kind, ApiError.KIND_API)
                self.assertEqual(e.http_status, status)
                self.assertTrue(e.retryable)

    def test_invalid_response(self):
        e = self.send(FakeTransport(502, b"<html><body>502 Bad Gateway</body></html>"))
        self.assertEqual(e.kind, ApiError.KIND_INVALID_RESPONSE)
        self.assertEqual(e.http_status, 502)
        self.assertTrue(e.retryable)
        self.assertIn("502 Bad Gateway", e.message)
        e = self.send(FakeTransport(200, b"not json"))
        self.assertEqual(e.kind, ApiError.KIND_INVALID_RESPONSE)
        self.assertFalse(e.retryable)

    def test_network_and_timeout(self):
        e = self.send(FakeTransport(error=ConnectionRefusedError("connection refused")))
        self.assertEqual(e.kind, ApiError.KIND_NETWORK)
        self.assertTrue(e.retryable)
        self.assertEqual(e.method, "email/send")
        self.assertIsInstance(e.__cause__, ConnectionRefusedError)
        e = self.send(FakeTransport(error=socket.timeout("timed out")))
        self.assertEqual(e.kind, ApiError.KIND_TIMEOUT)
        self.assertTrue(e.retryable)

    def test_empty_api_key(self):
        transport = FakeTransport()
        e = self.send(transport, api_key="")
        self.assertEqual(e.kind, ApiError.KIND_INVALID_REQUEST)
        self.assertFalse(e.retryable)
        self.assertEqual(e.http_status, 0)
        self.assertEqual(transport.calls, [])

    def test_required_fields(self):
        message = {"subject": "Hello", "from_email": "shop@example.com", "body": {"html": "<b>Hi</b>"}}
        cases = [
            ({**message}, "message.recipients"),
            ({**message, "recipients": []}, "message.recipients"),
            ({**message, "recipients": [{"email": ""}]}, "message.recipients[0].email"),
        ]
        for body, field in cases:
            with self.subTest(field=field, body=body):
                transport = FakeTransport()
                with self.assertRaises(ApiError) as caught:
                    make_client(transport).api_client.call("/email/send.json", {"message": body})
                e = caught.exception
                self.assertEqual(e.kind, ApiError.KIND_INVALID_REQUEST)
                self.assertEqual(e.message, "email/send: " + field + " is required")
                self.assertEqual(transport.calls, [])

    def test_long_api_message(self):
        text = "x" * 600
        e = self.send(json_error(400, text))
        self.assertEqual(e.api_message, text)
        self.assertIn("x" * 500 + "... (600 chars)", e.message)
        self.assertNotIn("x" * 501, e.message)

    def test_error_code_forms(self):
        self.assertEqual(self.send(json_error(400, code="204")).error_code, 204)
        self.assertIsNone(self.send(json_error(400, code="abc")).error_code)

    def test_transport_api_error_kept(self):
        own = ApiError("proxy refused", 407, 9, {"status": "error"}, hint="Check the proxy",
                       kind=ApiError.KIND_INVALID_RESPONSE, api_message="refused")
        e = self.send(FakeTransport(error=own))
        self.assertEqual((e.http_status, e.error_code, e.response_body, e.hint, e.kind, e.api_message),
                         (407, 9, {"status": "error"}, "Check the proxy", ApiError.KIND_INVALID_RESPONSE, "refused"))
        self.assertEqual(e.method, "email/send")
        self.assertEqual(e.message, "email/send: proxy refused")
        bare = self.send(FakeTransport(error=ApiError("down")))
        self.assertEqual(bare.kind, ApiError.KIND_NETWORK)
        self.assertTrue(bare.retryable)


class Handler(http.server.BaseHTTPRequestHandler):
    """The local API: answers every POST with the JSON of the server (status, body), after its delay."""

    def do_POST(self):
        server = self.server
        server.requests.append({"path": self.path, "headers": self.headers,
                                "body": self.rfile.read(int(self.headers.get("Content-Length") or 0))})
        time.sleep(server.delay)
        status, body = server.reply
        try:
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except OSError:
            pass  # the client has gone (timeout test)

    def log_message(self, *args):
        pass


class LocalServer(http.server.ThreadingHTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        pass


class UrllibTransportTest(unittest.TestCase):
    """The default transport against a server on 127.0.0.1 (proxies of the environment bypassed)."""

    def setUp(self):
        env = mock.patch.dict(os.environ, {"NO_PROXY": "*", "no_proxy": "*"})
        env.start()
        self.addCleanup(env.stop)
        self.server = LocalServer(("127.0.0.1", 0), Handler)
        self.server.requests, self.server.delay = [], 0
        self.server.reply = (200, b'{"status": "success", "job_id": "1ZymBc-00041N-9X"}')
        thread = threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
        thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.base_url = "http://127.0.0.1:%d/api/v1" % self.server.server_address[1]

    def client(self, timeout=5.0):
        return unione.client(API_KEY, self.base_url, timeout, transport=UrllibTransport())

    def test_success(self):
        response = self.client().email.send(send_request())
        self.assertEqual(response.job_id, "1ZymBc-00041N-9X")
        request = self.server.requests[0]
        self.assertTrue(request["path"].startswith("/api/v1/email/send.json?platform="))
        self.assertEqual(request["headers"]["X-API-KEY"], API_KEY)
        self.assertEqual(json.loads(request["body"])["message"]["subject"], "Hello")

    def test_http_error_status(self):
        self.server.reply = (400, b'{"status": "error", "message": "Unknown recipient", "code": 204}')
        with self.assertRaises(ApiError) as caught:
            self.client().email.send(send_request())
        self.assertEqual((caught.exception.http_status, caught.exception.error_code), (400, 204))

    def test_timeout(self):
        self.server.delay = 1.0
        with self.assertRaises(ApiError) as caught:
            self.client(timeout=0.2).email.send(send_request())
        self.assertEqual(caught.exception.kind, ApiError.KIND_TIMEOUT)
        self.assertTrue(caught.exception.retryable)

    def test_connection_refused(self):
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        client = unione.client(API_KEY, "http://127.0.0.1:%d/api/v1" % port, 5.0, transport=UrllibTransport())
        with self.assertRaises(ApiError) as caught:
            client.email.send(send_request())
        self.assertEqual(caught.exception.kind, ApiError.KIND_NETWORK)
        self.assertTrue(caught.exception.retryable)


class WebhookTest(unittest.TestCase):
    def test_parse_callback(self):
        callback = WebhookApi.parse_callback(json.dumps({
            "auth": "00000000000000000000000000000000",
            "events_by_user": [
                {
                    "events": [
                        {
                            "event_name": "transactional_email_status",
                            "event_data": {
                                "email": "alex@example.com",
                                "status": "delivered",
                            },
                        },
                    ],
                },
            ],
        }))
        self.assertEqual(callback.auth, "0" * 32)
        event = callback.events_by_user[0].events[0]
        self.assertEqual(event.event_data.email, "alex@example.com")


if __name__ == "__main__":
    unittest.main()
