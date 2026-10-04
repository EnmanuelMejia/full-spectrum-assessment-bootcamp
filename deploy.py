#!/usr/bin/env python3
"""Deploy the Full Spectrum bootcamp as a standalone Worker serving index.html
at /assessments/* and chat.html at /assessments/chat/*, then route those paths
on all three of the user's domains to it.

Usage: deploy.py
"""
import base64
import io
import json
import sys
import urllib.request
import urllib.error

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response  # noqa: E402

BASE = "https://api.cloudflare.com/client/v4"
ACCOUNT = "bb1baf6bc6c34d30fadc402b420fa3c2"
DIR = "/home/hatch/workspace/full-spectrum-bootcamp"
WORKER = "full-spectrum-bootcamp"


def api(method, path, body=None, headers=None):
    req = urllib.request.Request(
        BASE + path, data=body, method=method, headers=headers or {}
    )
    add_surrogate_to_request(
        req, credential_name="custom.cloudflare", allowed_hosts=["api.cloudflare.com"]
    )
    try:
        resp = urllib.request.urlopen(req, timeout=120)
    except urllib.error.HTTPError as e:
        print(json.dumps({"http_error": e.code, "body": e.read().decode()[:3000]}, indent=2))
        sys.exit(1)
    return read_json_response(resp)


def main():
    pages = {}
    for name in ("index.html", "chat.html"):
        with open(f"{DIR}/{name}", "rb") as f:
            pages[name] = f.read()
        print(f"{name} bytes: {len(pages[name])}")

    b64_index = base64.b64encode(pages["index.html"]).decode()
    b64_chat = base64.b64encode(pages["chat.html"]).decode()

    script = (
        'const IDX = "' + b64_index + '";\n'
        'const CHT = "' + b64_chat + '";\n'
        "function b64ToUtf8(b64) {\n"
        "  const bin = atob(b64);\n"
        "  const bytes = new Uint8Array(bin.length);\n"
        "  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);\n"
        "  return new TextDecoder().decode(bytes);\n"
        "}\n"
        "let I = null, C = null;\n"
        "export default {\n"
        "  async fetch(request) {\n"
        "    const url = new URL(request.url);\n"
        "    const isChat = url.pathname.startsWith('/assessments/chat');\n"
        "    if (isChat) { if (!C) C = b64ToUtf8(CHT); }\n"
        "    else { if (!I) I = b64ToUtf8(IDX); }\n"
        "    return new Response(isChat ? C : I, { headers: {\n"
        '      "content-type": "text/html;charset=UTF-8",\n'
        '      "cache-control": "public, max-age=3600"\n'
        "    }});\n"
        "  }\n"
        "};\n"
    )
    print(f"worker script bytes: {len(script)}")

    boundary = "----cfdeploy123456"
    metadata = json.dumps(
        {"main_module": "worker.js", "compatibility_date": "2026-09-25"}
    )
    buf = io.BytesIO()
    buf.write(f"--{boundary}\r\n".encode())
    buf.write(b'Content-Disposition: form-data; name="metadata"\r\n')
    buf.write(b"Content-Type: application/json\r\n\r\n")
    buf.write(metadata.encode() + b"\r\n")
    buf.write(f"--{boundary}\r\n".encode())
    buf.write(b'Content-Disposition: form-data; name="worker.js"; filename="worker.js"\r\n')
    buf.write(b"Content-Type: application/javascript+module\r\n\r\n")
    buf.write(script.encode() + b"\r\n")
    buf.write(f"--{boundary}--\r\n".encode())

    r = api(
        "PUT",
        f"/accounts/{ACCOUNT}/workers/scripts/{WORKER}",
        body=buf.getvalue(),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    print("worker upload:", json.dumps(r)[:500])

    zones = {
        "enmanueldmejia.com": "c17e24dfb06602421aefb6d8e88e60c2",
        "interstitiumlabs.dev": "3f705489afbb4d6ed20b777e2d027047",
    }
    for host, zone_id in zones.items():
        targets = [host] if host != "interstitiumlabs.dev" else [host, f"learn.{host}"]
        for h in targets:
            pattern = f"{h}/assessments/*"
            r = api(
                "POST",
                f"/zones/{zone_id}/workers/routes",
                body=json.dumps({"pattern": pattern, "script": WORKER}).encode(),
                headers={"Content-Type": "application/json"},
            )
            ok = r.get("success")
            print(f"route {pattern}: {'OK' if ok else json.dumps(r)[:400]}")


if __name__ == "__main__":
    main()
