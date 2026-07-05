from datetime import datetime
from typing import List, Optional
from src.models.core_entities import AuditRecord

class AuditLogger:
    """
    Responsible for recording immutable audit records.
    Adheres to RFC-0007 (Execution Record Model) and Article 7 of the Constitution.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuditLogger, cls).__new__(cls)
            cls._instance.records: List[AuditRecord] = []
            print("--> AuditLogger Initialized: Ready for recording.")
        return cls._instance
    
    def log(self, 
            source_component: str, 
            severity: str, 
            message: str, 
            related_ids: Optional[List[str]] = None) -> None:
        """
        Records a new audit event.
        
        Args:
            source_component: The component making the log entry (e.g., 'PolicyEngine', 'Executor')
            severity: The severity level ('INFO', 'WARNING', 'CRITICAL')
            message: Description of the event
            related_ids: Optional list of related goal/task IDs
        """
        record = AuditRecord(
            source_component=source_component,
            severity=severity,
            message=message,
            timestamp=datetime.now(),
            related_ids=related_ids or []
        )
        self.records.append(record)
        print(f"[AUDIT] {record.timestamp.isoformat()} | {source_component} | {severity}: {message}")
    
    def get_records(self, 
                    source_component: Optional[str] = None,
                    severity: Optional[str] = None) -> List[AuditRecord]:
        """
        Retrieves audit records, optionally filtered by component or severity.
        """
        results = self.records
        if source_component:
            results = [r for r in results if r.source_component == source_component]
        if severity:
            results = [r for r in results if r.severity == severity]
        return results
    
    def get_all_records(self) -> List[AuditRecord]:
        """Returns all audit records."""
        return self.records

# Singleton access
audit_logger = AuditLogger()
