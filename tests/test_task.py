from dataclasses import FrozenInstanceError

import pytest

from ai_kernel.model.task import Task


def test_task_has_unique_id():
    t1 = Task("hello")
    t2 = Task("hello")

    assert t1.id != t2.id


def test_task_is_immutable():
    task = Task("hello")

    with pytest.raises(FrozenInstanceError):
        task.objective = "world"


def test_metadata_is_readonly():
    task = Task(
        "hello",
        metadata={"foo": "bar"},
    )

    with pytest.raises(TypeError):
        task.metadata["foo"] = "baz"


def test_objective_is_preserved():
    task = Task("Write README")

    assert task.objective == "Write README"
