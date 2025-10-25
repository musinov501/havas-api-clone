import logging
from typing import Dict

from .accounts import ACCOUNT_MESSAGES
from .shared import SHARED_MESSAGES
from .types import MessageTemplate

logger = logging.getLogger(__name__)

# Combine all message dictionaries
MESSAGES: Dict[str, MessageTemplate] = {
    **SHARED_MESSAGES,
    **ACCOUNT_MESSAGES
}


# Validate for duplicate keys during module import
def _validate_messages():
    """Check for duplicate message keys across different modules"""
    all_keys = []
    message_sources = [
        ("SHARED_MESSAGES", SHARED_MESSAGES),
        ("ACCOUNT_MESSAGES", ACCOUNT_MESSAGES),
    ]

    duplicates = []
    for source_name, messages in message_sources:
        for key in messages.keys():
            if key in all_keys:
                duplicates.append(f"{key} (found in {source_name})")
            all_keys.append(key)

    if duplicates:
        logger.error(f"Duplicate message keys found: {', '.join(duplicates)}")
        # In development, raise exception. In production, log only.
        # raise ValueError(f"Duplicate message keys: {duplicates}")


# Run validation on import
_validate_messages()

# Export types and messages
__all__ = [
    'MESSAGES',
    'MessageTemplate',
    'SHARED_MESSAGES',
    'ACCOUNT_MESSAGES'
]
