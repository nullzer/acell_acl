from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum


class WorkMode(StrEnum):
    LOCAL = "local"
    NETWORK = "network"


class ModeState(StrEnum):
    READY = "ready"
    NEEDS_NETWORK_RESOURCE = "needs_network_resource"


@dataclass(frozen=True)
class PlatformRequirement:
    name: str
    description: str


@dataclass(frozen=True)
class AppState:
    mode: WorkMode = WorkMode.LOCAL
    network_resource_path: str = ""


@dataclass(frozen=True)
class ModeStatus:
    state: ModeState
    title: str
    details: str


SUPPORTED_PLATFORMS: tuple[PlatformRequirement, ...] = (
    PlatformRequirement(
        name="Windows 10",
        description="Локальный запуск приложения на рабочих местах пользователей Windows 10.",
    ),
    PlatformRequirement(
        name="ALT Linux",
        description="Локальный запуск приложения в среде ALT Linux без изменения сценариев работы.",
    ),
)

DEVELOPMENT_STAGES: tuple[str, ...] = (
    "Уточнение требований",
    "Проектирование",
    "Прототипирование интерфейса",
    "Разработка локальной версии",
    "Сборка под ALT Linux и Windows 10",
    "Тестирование",
    "Подготовка к внедрению",
)


def set_work_mode(state: AppState, mode: WorkMode) -> AppState:
    return replace(state, mode=mode)


def set_network_resource_path(state: AppState, path: str) -> AppState:
    return replace(state, network_resource_path=path.strip())


def get_mode_status(state: AppState) -> ModeStatus:
    if state.mode is WorkMode.LOCAL:
        return ModeStatus(
            state=ModeState.READY,
            title="Локальный режим готов",
            details="Приложение работает на текущем компьютере и использует локальное размещение данных.",
        )

    if not state.network_resource_path:
        return ModeStatus(
            state=ModeState.NEEDS_NETWORK_RESOURCE,
            title="Укажите сетевой ресурс",
            details="Многопользовательский режим доступен только при размещении данных на сетевом ресурсе.",
        )

    return ModeStatus(
        state=ModeState.READY,
        title="Сетевой режим готов",
        details=f"Работа будет выполняться через сетевой ресурс: {state.network_resource_path}.",
    )
