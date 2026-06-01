export type WorkMode = 'local' | 'network';

export type ModeState = 'ready' | 'needs-network-resource';

export interface PlatformRequirement {
  readonly name: string;
  readonly description: string;
}

export interface AppState {
  readonly mode: WorkMode;
  readonly networkResourcePath: string;
}

export interface ModeStatus {
  readonly state: ModeState;
  readonly title: string;
  readonly details: string;
}

export const supportedPlatforms: readonly PlatformRequirement[] = [
  {
    name: 'Windows 10',
    description: 'Поддержка запуска на рабочих местах пользователей Windows 10.',
  },
  {
    name: 'ALT Linux',
    description: 'Поддержка запуска в среде ALT Linux без изменения сценариев работы.',
  },
];

export const developmentStages: readonly string[] = [
  'Уточнение требований',
  'Проектирование',
  'Прототипирование интерфейса',
  'Разработка базовой версии',
  'Реализация многопользовательского режима',
  'Тестирование',
  'Подготовка к внедрению',
  'Приемка и сопровождение',
];

export const initialState: AppState = {
  mode: 'local',
  networkResourcePath: '',
};

export const setWorkMode = (state: AppState, mode: WorkMode): AppState => ({
  ...state,
  mode,
});

export const setNetworkResourcePath = (state: AppState, path: string): AppState => ({
  ...state,
  networkResourcePath: path.trim(),
});

export const getModeStatus = (state: AppState): ModeStatus => {
  if (state.mode === 'local') {
    return {
      state: 'ready',
      title: 'Однопользовательский режим готов',
      details: 'Приложение использует локальное размещение данных на рабочем месте пользователя.',
    };
  }

  if (!state.networkResourcePath) {
    return {
      state: 'needs-network-resource',
      title: 'Укажите сетевой ресурс',
      details: 'Многопользовательский режим доступен только при размещении приложения и/или данных на сетевом ресурсе.',
    };
  }

  return {
    state: 'ready',
    title: 'Многопользовательский режим готов',
    details: `Работа будет выполняться через сетевой ресурс: ${state.networkResourcePath}.`,
  };
};
