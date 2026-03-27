from reversible_redaction.redactor import redact_text


def test_redact_removes_sensitive_values():
    original = "IP 10.1.2.3 belongs to kpw_proxy_72"
    redacted, mappings = redact_text(original)
    assert "10.1.2.3" not in redacted
    assert "kpw_proxy_72" not in redacted
    assert mappings
