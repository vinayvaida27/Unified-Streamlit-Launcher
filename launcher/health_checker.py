"""Streamlit health polling."""

from __future__ import annotations

from pathlib import Path
import time
from subprocess import Popen
import re
from urllib.error import URLError
from urllib.request import urlopen

from .constants import HEALTH_PATH
from .exceptions import ApplicationHealthCheckError


class HealthChecker:
    """Polls a Streamlit server until it is healthy."""

    def wait_until_healthy(self, process: Popen, port: int, timeout_seconds: int, log_path: Path | None = None) -> str:
        """Wait for health endpoint and return the root URL."""

        root_url = f"http://127.0.0.1:{port}"
        health_url = f"{root_url}{HEALTH_PATH}"
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            exit_code = process.poll()
            if exit_code is not None:
                raise ApplicationHealthCheckError(f"Streamlit exited before becoming healthy with code {exit_code}")
            if log_path:
                ready_url = self.streamlit_ready_url_from_log(log_path)
                if ready_url:
                    return ready_url
            if self._url_ok(health_url) or self._url_ok(root_url):
                return root_url
            time.sleep(0.1)
        raise ApplicationHealthCheckError(f"Application did not become healthy within {timeout_seconds} seconds")

    @staticmethod
    def _url_ok(url: str) -> bool:
        try:
            with urlopen(url, timeout=0.2) as response:
                return 200 <= int(response.status) < 500
        except (OSError, URLError):
            return False

    @staticmethod
    def _streamlit_log_reports_ready(log_path: Path, root_url: str) -> bool:
        """Return true when Streamlit has written its ready URL to the app log."""

        return HealthChecker.streamlit_ready_url_from_log(log_path) == root_url

    @staticmethod
    def streamlit_ready_url_from_log(log_path: Path) -> str | None:
        """Return the latest ready localhost URL written by Streamlit."""

        try:
            text = log_path.read_text(encoding="utf-8", errors="replace")[-8000:]
        except OSError:
            return None
        if "You can now view your Streamlit app in your browser." not in text:
            return None
        ready_urls = re.findall(r"https?://127\.0\.0\.1:\d+", text)
        return ready_urls[-1] if ready_urls else None
