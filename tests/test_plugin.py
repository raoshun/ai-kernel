from ai_kernel.kernel.core import Kernel
from ai_kernel.plugin import BasePlugin


class InitializingPlugin(BasePlugin):
    def __init__(self, identifier: str):
        super().__init__(identifier)
        self.initialized = False

    def initialize(self) -> None:
        self.initialized = True


class FailingPlugin(BasePlugin):
    def __init__(self, identifier: str):
        super().__init__(identifier)
        self.initialized = False

    def initialize(self) -> None:
        self.initialized = True
        raise RuntimeError("boom")


def test_plugin_registration_and_retrieval():
    kernel = Kernel()
    plugin = BasePlugin("demo", name="Demo Plugin")

    assert kernel.register_plugin(plugin)
    assert kernel.get_plugins()["demo"] is plugin


def test_duplicate_registration_is_rejected():
    kernel = Kernel()

    assert kernel.register_plugin(BasePlugin("demo"))
    assert not kernel.register_plugin(BasePlugin("demo"))
    assert len(kernel.get_plugins()) == 1


def test_unregister_plugin_removes_registration():
    kernel = Kernel()
    plugin = BasePlugin("demo")

    kernel.register_plugin(plugin)

    assert kernel.unregister_plugin("demo")
    assert "demo" not in kernel.get_plugins()


def test_initialize_plugins_continues_after_failures():
    kernel = Kernel()
    plugin_a = InitializingPlugin("a")
    plugin_b = FailingPlugin("b")
    plugin_c = InitializingPlugin("c")

    kernel.register_plugin(plugin_a)
    kernel.register_plugin(plugin_b)
    kernel.register_plugin(plugin_c)

    kernel.initialize_plugins()

    assert plugin_a.initialized
    assert plugin_b.initialized
    assert plugin_c.initialized
