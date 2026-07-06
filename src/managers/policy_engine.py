from typing import List, Dict

from models.core_entities import Authority, Capability, Permission
from managers.capability_manager import capability_manager

from ai_kernel._logging import manager_logger

class PolicyEngine:
    """
    The central authority for determining if an action is permitted.
    Adheres strictly to the Separation of Authority and Least Privilege (RFC-0001).
    """
    def __init__(self):
        # 依存性注入: システムのCapabilityレジストリを利用
        self.capability_manager = capability_manager
        # 実際のポリシーセット（ロードされるべき設定）
        self._policies: Dict[str, List[Permission]] = {}
        manager_logger.info("PolicyEngine initialized: Awaiting policy rules definition.")
    
    def load_policy(self, principal_id: str, policies: List[Permission]) -> None:
        """Loads a set of permissions for a specific Principal ID/Role combination."""
        # 実際には、より複雑なロールベースの階層構造が必要だが、MVPとしてシンプルに実装
        self._policies[principal_id] = policies
        manager_logger.info(f"Successfully loaded {len(policies)} permissions for Principal ID: {principal_id}")

    def check_permission(self, authority: Authority, required_capability: Capability) -> bool:
        """
        Checks if the given authority has an explicit ALLOW permission for the required capability.
        Returns True only if explicitly permitted by loaded policies.
        """
        manager_logger.info(f"Checking {authority.role} ({authority.principal_id}) for capability '{required_capability.name}'...")
        
        if authority.principal_id not in self._policies:
            manager_logger.warning("No policies found for this Principal ID.")
            return False

        for permission in self._policies[authority.principal_id]:
            # 1. Capabilityが要求されているものと一致するか確認 (Required -> Target)
            if permission.target_capability != required_capability:
                continue
            
            # 2. 効果（Effect）が許可か、かつアクションが合致するか確認
            # ここではシンプルに 'ALLOW' かつアクションの一致を要求する
            if permission.effect == 'ALLOW':
                 manager_logger.info(f"Allowed: Explicitly permitted via {permission.action} using '{required_capability.name}'.")
                 return True
        
        manager_logger.warning("No explicit ALLOW permission found for this combination.")
        return False

# Factory function for lazy initialization
_policy_engine_instance = None

def get_policy_engine() -> PolicyEngine:
    """Get the singleton PolicyEngine instance."""
    global _policy_engine_instance
    if _policy_engine_instance is None:
        _policy_engine_instance = PolicyEngine()
    return _policy_engine_instance

# Backward compatibility alias
policy_engine = get_policy_engine()


