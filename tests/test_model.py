import unittest

from acell_acl.model import (
    SUPPORTED_PLATFORMS,
    AppState,
    ModeState,
    WorkMode,
    get_mode_status,
    set_network_resource_path,
    set_work_mode,
)


class AppModelTest(unittest.TestCase):
    def test_supported_platforms_are_windows_10_and_alt_linux(self) -> None:
        self.assertEqual([platform.name for platform in SUPPORTED_PLATFORMS], ["Windows 10", "ALT Linux"])

    def test_local_mode_is_ready_by_default(self) -> None:
        status = get_mode_status(AppState())

        self.assertIs(status.state, ModeState.READY)
        self.assertEqual(status.title, "Локальный режим готов")

    def test_network_mode_requires_resource_path(self) -> None:
        state = set_work_mode(AppState(), WorkMode.NETWORK)
        status = get_mode_status(state)

        self.assertIs(status.state, ModeState.NEEDS_NETWORK_RESOURCE)
        self.assertEqual(status.title, "Укажите сетевой ресурс")

    def test_network_mode_is_ready_with_resource_path(self) -> None:
        state = set_network_resource_path(set_work_mode(AppState(), WorkMode.NETWORK), "  \\\\server\\share  ")
        status = get_mode_status(state)

        self.assertIs(status.state, ModeState.READY)
        self.assertEqual(status.title, "Сетевой режим готов")
        self.assertIn("\\\\server\\share", status.details)


if __name__ == "__main__":
    unittest.main()
