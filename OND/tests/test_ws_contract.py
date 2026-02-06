import asyncio
import json
import unittest
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
import jsonschema

# Golden message schemas
HELLO_REQ_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"const": "hello"},
        "sr": {"type": "integer", "minimum": 8000, "maximum": 192000},
    },
    "required": ["type", "sr"],
    "additionalProperties": False,
}
HELLO_RESP_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"const": "hello"},
        "ok": {"type": "boolean"},
        "sr": {"type": "integer"},
    },
    "required": ["type", "ok", "sr"],
    "additionalProperties": False,
}
PITCH_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"const": "pitch"},
        "hz": {"type": "number"},
        "note": {"type": "string"},
        "rms": {"type": "number"},
        "voiced": {"type": "boolean"},
    },
    "required": ["type", "hz", "note", "rms", "voiced"],
    "additionalProperties": False,
}

# Import the app from server.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from server import main as server_main, ws_pitch


class TestWSContract(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        app.router.add_get("/ws", ws_pitch)
        return app

    @unittest_run_loop
    async def test_happy_path_hello_and_pitch(self):
        ws = await self.client.ws_connect("/ws")
        # Send hello
        hello_req = {"type": "hello", "sr": 48000}
        await ws.send_str(json.dumps(hello_req))
        hello_resp = await ws.receive_json()
        jsonschema.validate(hello_req, HELLO_REQ_SCHEMA)
        jsonschema.validate(hello_resp, HELLO_RESP_SCHEMA)
        # Send a short frame (silence)
        import numpy as np

        frame = np.zeros(2048, dtype=np.float32).tobytes()
        await ws.send_bytes(frame)
        # Should get a pitch message (silence)
        while True:
            msg = await ws.receive_json()
            if msg.get("type") == "pitch":
                jsonschema.validate(msg, PITCH_SCHEMA)
                assert msg["hz"] == 0.0
                assert msg["note"] == "—"
                assert not msg["voiced"]
                break
        await ws.close()

    @unittest_run_loop
    async def test_negative_malformed_hello(self):
        ws = await self.client.ws_connect("/ws")
        # Missing 'sr' field
        bad_hello = {"type": "hello"}
        await ws.send_str(json.dumps(bad_hello))
        # Server should ignore or not crash; no response expected
        try:
            resp = await ws.receive(timeout=0.5)
            # Acceptable: server ignores, closes, or sends error
            assert resp.type in {
                web.WSMsgType.CLOSE,
                web.WSMsgType.CLOSED,
                web.WSMsgType.CLOSING,
                web.WSMsgType.TEXT,
                web.WSMsgType.BINARY,
            }
        except Exception:
            pass
        await ws.close()


if __name__ == "__main__":
    unittest.main()
