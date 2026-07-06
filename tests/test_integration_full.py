"""
Integration Tests - Comprehensive tests of the refactored kernel system.

Tests the full workflow:
1. Kernel creation via factory
2. Goal processing with WorkflowCoordinator
3. Manager delegation (Planning, Risk Assessment, Authorization, Execution, Audit)
4. Validation and review
5. Status reporting
"""
from kernel.core import Kernel, WorkflowCoordinator, create_kernel
from models.core_entities import Goal, Authority, Task, ExecutionStep
from managers.validation_helper import ExecutionValidator
from managers.reviewer import Reviewer
from managers.audit_logger import get_audit_logger


class TestKernelIntegration:
    """Integration tests for Kernel functionality."""
    
    def test_kernel_factory_creation(self):
        """Test that create_kernel factory works correctly."""
        kernel = create_kernel('test_user', 'ADMIN')
        assert kernel.user_authority.principal_id == 'test_user'
        assert kernel.user_authority.role == 'ADMIN'
    
    def test_workflow_coordinator_initialization(self):
        """Test WorkflowCoordinator initialization."""
        authority = Authority(principal_id='test_user', role='USER')
        coordinator = WorkflowCoordinator(authority)
        assert coordinator.authority.principal_id == 'test_user'
    
    def test_goal_processing_workflow(self):
        """Test complete goal processing workflow."""
        kernel = create_kernel('test_user', 'USER')
        goal = Goal(
            goal_id='test-goal-001',
            description='Test workflow execution',
            expected_output_format='plain_text'
        )
        
        result = kernel.process_goal(goal)
        
        assert result['status'] == 'COMPLETED'
        assert result['goal_id'] == 'test-goal-001'
        assert 'risk_assessment' in result
    
    def test_kernel_status_reporting(self):
        """Test kernel status reporting."""
        kernel = create_kernel('test_user', 'ADMIN')
        status = kernel.get_status()
        
        assert status['user'] == 'test_user'
        assert 'registered_capabilities' in status
        assert 'audit_records' in status
    
    def test_multiple_goal_processing(self):
        """Test processing multiple goals sequentially."""
        kernel = create_kernel('test_user', 'ADMIN')
        
        for i in range(3):
            goal = Goal(
                goal_id=f'goal-{i}',
                description=f'Test goal {i}',
                expected_output_format='json'
            )
            result = kernel.process_goal(goal)
            assert result['status'] == 'COMPLETED'
        
        status = kernel.get_status()
        # Should have audit records from all 3 goals
        assert status['audit_records'] >= 3


class TestExecutionValidator:
    """Integration tests for ExecutionValidator."""
    
    def test_error_detection_workflow(self):
        """Test error detection in realistic execution steps."""
        steps = [
            ExecutionStep(tool_name='read_file', input_params={}, actual_output='File content here'),
            ExecutionStep(tool_name='parse_json', input_params={}, actual_output='Error: Invalid JSON format'),
            ExecutionStep(tool_name='save_result', input_params={}, actual_output=''),
        ]
        
        validation = ExecutionValidator.validate_execution_steps(steps)
        
        assert validation['total_steps'] == 3
        assert validation['successful_steps'] == 1
        assert validation['error_steps'] == 1
        assert validation['warning_steps'] == 1
        assert len(validation['issues']) > 0
    
    def test_status_classification_workflow(self):
        """Test status classification for different scenarios."""
        # All successful
        status = ExecutionValidator.classify_overall_status(0, 0, 5)
        assert status == 'SUCCESS'
        
        # Some warnings
        status = ExecutionValidator.classify_overall_status(0, 2, 3)
        assert status == 'PARTIAL'
        
        # Any errors
        status = ExecutionValidator.classify_overall_status(1, 0, 4)
        assert status == 'FAILED'


class TestReviewerIntegration:
    """Integration tests for Reviewer."""
    
    def test_task_review_workflow(self):
        """Test reviewing a single task execution."""
        reviewer = Reviewer()
        task = Task(
            task_id='task-001',
            description='Test task',
            required_capabilities=['read_file'],
            dependencies=[]
        )
        steps = [
            ExecutionStep(tool_name='read_file', input_params={}, actual_output='Success'),
        ]
        
        review = reviewer.review_task_execution(task, steps)
        
        assert review['task_id'] == 'task-001'
        assert review['status'] == 'SUCCESS'
        assert review['steps_executed'] == 1
        assert isinstance(review['recommendations'], list)
    
    def test_plan_review_workflow(self):
        """Test reviewing a complete plan execution."""
        reviewer = Reviewer()
        tasks = [
            Task(task_id='task-1', description='Step 1', required_capabilities=[], dependencies=[]),
            Task(task_id='task-2', description='Step 2', required_capabilities=[], dependencies=['task-1']),
            Task(task_id='task-3', description='Step 3', required_capabilities=[], dependencies=[]),
        ]
        
        execution_results = [
            [ExecutionStep(tool_name='tool1', input_params={}, actual_output='Success')],
            [ExecutionStep(tool_name='tool2', input_params={}, actual_output='Error occurred')],
            [],
        ]
        
        review = reviewer.review_plan_execution(tasks, execution_results)
        
        assert review['total_tasks'] == 3
        assert review['overall_status'] == 'FAILED'
        assert len(review['task_reviews']) == 3
        assert isinstance(review['overall_recommendations'], list)


class TestAuditLogging:
    """Integration tests for audit logging."""
    
    def test_audit_trail_accumulation(self):
        """Test that audit records accumulate from all components."""
        audit_logger = get_audit_logger()
        
        # Clear previous records for test isolation
        initial_count = len(audit_logger.get_all_records())
        
        # Process goals which should generate audit records
        kernel = create_kernel('test_user', 'ADMIN')
        goal = Goal(
            goal_id='audit-test-001',
            description='Test audit logging',
            expected_output_format='plain_text'
        )
        kernel.process_goal(goal)
        
        # Verify audit records were created
        final_count = len(audit_logger.get_all_records())
        assert final_count > initial_count
    
    def test_audit_record_filtering(self):
        """Test filtering audit records by component."""
        audit_logger = get_audit_logger()
        
        # Log from different components
        audit_logger.log('Component1', 'INFO', 'Test message 1', [])
        audit_logger.log('Component2', 'WARNING', 'Test message 2', [])
        
        # Filter by component
        comp1_records = audit_logger.get_records(source_component='Component1')
        comp2_records = audit_logger.get_records(source_component='Component2')
        
        assert len(comp1_records) > 0
        assert len(comp2_records) > 0


if __name__ == '__main__':
    # Simple test runner for manual execution
    print("Running integration tests...")
    
    test_kernel = TestKernelIntegration()
    test_kernel.test_kernel_factory_creation()
    print("✓ test_kernel_factory_creation")
    
    test_kernel.test_workflow_coordinator_initialization()
    print("✓ test_workflow_coordinator_initialization")
    
    test_kernel.test_goal_processing_workflow()
    print("✓ test_goal_processing_workflow")
    
    test_kernel.test_kernel_status_reporting()
    print("✓ test_kernel_status_reporting")
    
    test_kernel.test_multiple_goal_processing()
    print("✓ test_multiple_goal_processing")
    
    test_validator = TestExecutionValidator()
    test_validator.test_error_detection_workflow()
    print("✓ test_error_detection_workflow")
    
    test_validator.test_status_classification_workflow()
    print("✓ test_status_classification_workflow")
    
    test_reviewer = TestReviewerIntegration()
    test_reviewer.test_task_review_workflow()
    print("✓ test_task_review_workflow")
    
    test_reviewer.test_plan_review_workflow()
    print("✓ test_plan_review_workflow")
    
    test_audit = TestAuditLogging()
    test_audit.test_audit_trail_accumulation()
    print("✓ test_audit_trail_accumulation")
    
    test_audit.test_audit_record_filtering()
    print("✓ test_audit_record_filtering")
    
    print("\n✓ All integration tests passed!")
