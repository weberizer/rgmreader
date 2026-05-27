#!/usr/bin/env python3
"""
Encripta home + analyzer con AES-GCM y los embebe en un nuevo index.html
con un login gate. Para cambiar la password después, edita PASSWORD abajo
y vuelve a correr este script.

Uso:
    python3 encrypt_site.py
    # luego: git add . && git commit -m "rotate password" && git push
"""

import os
import base64
import json
import secrets
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ─── CONFIGURACIÓN ──────────────────────────────────────────────────────
USERNAME = "admin1Benito"
PASSWORD = "Animalrgmdallas26!"   # ← change me and re-run the script to rotate
PBKDF2_ITERATIONS = 250_000     # robusta vs ataques de fuerza bruta offline
# ────────────────────────────────────────────────────────────────────────

# Source files (these are the unencrypted originals — keep them OUT of git)
SRC_HOME     = "_src/home.html"
SRC_ANALYZER = "_src/analyzer.html"
OUTPUT       = "index.html"
TEMPLATE     = "_src/gate_template.html"

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))

def encrypt(plaintext: str, password: str) -> str:
    """Returns base64( salt || nonce || ciphertext+tag )."""
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    ct = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    return base64.b64encode(salt + nonce + ct).decode("ascii")

def main():
    # Read source HTMLs
    with open(SRC_HOME, encoding="utf-8") as f:
        home_html = f.read()
    with open(SRC_ANALYZER, encoding="utf-8") as f:
        analyzer_html = f.read()
    with open(TEMPLATE, encoding="utf-8") as f:
        template = f.read()

    # Combine username+password to derive the effective password (so both must match)
    effective_pw = f"{USERNAME}::{PASSWORD}"

    payload = {
        "iter": PBKDF2_ITERATIONS,
        "username": USERNAME,  # cosmetic: shown in login form
        "home": encrypt(home_html, effective_pw),
        "analyzer": encrypt(analyzer_html, effective_pw),
    }

    # Inject payload into template
    payload_json = json.dumps(payload).replace("</", "<\\/")
    rendered = template.replace("__PAYLOAD__", payload_json)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"✓ Encrypted home ({len(home_html):,} chars) and analyzer ({len(analyzer_html):,} chars)")
    print(f"✓ Wrote {OUTPUT} ({len(rendered):,} chars)")
    print(f"✓ Username: {USERNAME}")
    print(f"✓ Password set (length {len(PASSWORD)})")

if __name__ == "__main__":
    main()
