import {
  getModeStatus,
  initialState,
  setNetworkResourcePath,
  setWorkMode,
  supportedPlatforms,
} from './app';

describe('application state', () => {
  it('lists Windows 10 and ALT Linux as supported platforms', () => {
    expect(supportedPlatforms.map((platform) => platform.name)).toEqual(['Windows 10', 'ALT Linux']);
  });

  it('starts in local single-user mode', () => {
    expect(getModeStatus(initialState)).toMatchObject({
      state: 'ready',
      title: 'Однопользовательский режим готов',
    });
  });

  it('requires a network resource for multi-user mode', () => {
    const state = setWorkMode(initialState, 'network');

    expect(getModeStatus(state)).toMatchObject({
      state: 'needs-network-resource',
      title: 'Укажите сетевой ресурс',
    });
  });

  it('enables multi-user mode after setting a network resource', () => {
    const state = setNetworkResourcePath(setWorkMode(initialState, 'network'), '  \\\\server\\share  ');

    expect(getModeStatus(state)).toEqual({
      state: 'ready',
      title: 'Многопользовательский режим готов',
      details: 'Работа будет выполняться через сетевой ресурс: \\\\server\\share.',
    });
  });
});
