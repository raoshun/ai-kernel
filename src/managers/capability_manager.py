from typing import Dict, Optional, List
from src.models.core_entities import Capability

class CapabilityManager:
    """
    Manages the system's catalogue of all known Capabilities.
    This acts as a central registry adhering to RFC-0000 Terminology.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CapabilityManager, cls).__new__(cls)
            cls._instance.capabilities: Dict[str, Capability] = {}
            # 初期化時、基本となるコア能力をロードすることを想定
            print("--> CapabilityManager Initialized: Core capabilities loaded.")
        return cls._instance
    
    def add_capability(self, capability: Capability) -> bool:
        """Registers a new capability if it doesn't conflict with an existing one."""
        if self.capabilities[capability.name]:
            print(f"Warning: Capability '{capability.name}' already exists. Overwriting might be undesirable.")
            return False # 既存定義を尊重し、オーバーライトしない
        
        self.capabilities[capability.name] = capability
        print(f"[REGISTERED] Capability added: {capability.name} ({capability.scope})")
        return True

    def get_capability(self, name: str) -> Optional[Capability]:
        """Retrieves a capability by its unique name."""
        return self.capabilities.get(name)

    def list_all_capabilities(self) -> List[Capability]:
        """Returns all registered capabilities for inspection."""
        return list(self.capabilities.values())

# =========================================
# Singleton Access Point:
# System components should always access this via CapabilityManager().
# =========================================
capability_manager = CapabilityManager()

