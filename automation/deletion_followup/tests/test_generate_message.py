from datetime import datetime, timezone
from pathlib import Path

import pytest

from generate_message import (
    GrafanaMetrics,
    choose_variant,
    format_number,
    humanize_when,
    parse_iso,
)


def test_format_number_handles_thresholds():
    assert format_number(None) is None
    assert format_number(0) == "0"
    assert format_number(42) == "42"
    assert format_number(1500) == "1,500"
    assert format_number(1_200_000) == "1.2M"


def test_parse_iso_normalizes_to_utc():
    parsed = parse_iso("2026-03-15T09:00:00Z")
    assert parsed.tzinfo is not None
    assert parsed.utcoffset().total_seconds() == 0


def test_humanize_when_buckets():
    now = datetime(2026, 5, 11, 12, 0, tzinfo=timezone.utc)
    assert humanize_when(now, now=now) == "earlier today"
    assert humanize_when(datetime(2026, 5, 10, 12, 0, tzinfo=timezone.utc), now=now) == "yesterday"
    assert humanize_when(datetime(2026, 5, 5, 12, 0, tzinfo=timezone.utc), now=now) == "6 days ago"


def test_choose_variant_with_usage_thresholds():
    thresholds = {"min_total_queries": 1000, "min_active_days": 7}

    high_usage = GrafanaMetrics(total_queries=50_000)
    assert choose_variant(high_usage, db_lifetime_days=2, thresholds=thresholds, forced=None) == "a"

    long_lifetime = GrafanaMetrics(total_queries=10)
    assert choose_variant(long_lifetime, db_lifetime_days=14, thresholds=thresholds, forced=None) == "a"

    low_usage = GrafanaMetrics(total_queries=10)
    assert choose_variant(low_usage, db_lifetime_days=2, thresholds=thresholds, forced=None) == "b"


def test_choose_variant_respects_forced():
    thresholds = {"min_total_queries": 1000, "min_active_days": 7}
    high_usage = GrafanaMetrics(total_queries=50_000)
    assert choose_variant(high_usage, db_lifetime_days=30, thresholds=thresholds, forced="b") == "b"
