# Security

Trust boundary:

Trusted:

- signed launcher release;
- approved application manifests;
- approved bundled runtime;
- read-only published release folder.

Untrusted:

- user-entered file paths;
- malformed manifests;
- incomplete network copies;
- arbitrary scripts outside registered app roots;
- environment variables that attempt path traversal.

The launcher rejects path traversal, absolute app entrypoints outside app roots, unsupported app types, invalid app IDs, and arbitrary command fields in manifests. Streamlit binds only to `127.0.0.1`; process launch never uses `shell=True`.
