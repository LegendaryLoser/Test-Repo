"""Reusable known-good seed specs for mutation testing."""

from __future__ import annotations

from ..history_helpers import req_block, spec_file_text


def single_req_seed(req_id: str = "REQ-AUTH-0001") -> str:
    return spec_file_text(req_block(req_id))


def two_req_seed(req_a: str = "REQ-AUTH-0001", req_b: str = "REQ-AUTH-0002") -> str:
    return spec_file_text(req_block(req_a), req_block(req_b))
