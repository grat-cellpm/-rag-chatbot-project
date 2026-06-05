def get_refusal_message() -> str:
    """
    Returns the strict, hardcoded refusal message for advisory queries.
    """
    return "Facts-only. No investment advice. Please consult a registered financial advisor or visit official AMFI/SEBI resources."

def get_pii_blocked_message() -> str:
    """
    Returns the message shown when a query contains sensitive PII.
    """
    return "Your query contains sensitive personal information (PII). For your security, this query has been blocked."
