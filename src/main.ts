import {
  developmentStages,
  getModeStatus,
  initialState,
  setNetworkResourcePath,
  setWorkMode,
  supportedPlatforms,
  type AppState,
  type WorkMode,
} from './app';
import './style.css';

let state: AppState = initialState;

const appElement = document.querySelector<HTMLDivElement>('#app');

if (!appElement) {
  throw new Error('App root element was not found.');
}

const escapeHtml = (value: string) =>
  value
    .replaceAll('&', '&amp;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');

const renderStatusCard = () => {
  const modeStatus = getModeStatus(state);

  return `
    <aside class="status-card status-card--${modeStatus.state}">
      <span class="status-card__label">Статус</span>
      <strong>${escapeHtml(modeStatus.title)}</strong>
      <p>${escapeHtml(modeStatus.details)}</p>
    </aside>
  `;
};

const refreshStatusCard = () => {
  const statusCard = appElement.querySelector<HTMLElement>('.status-card');

  if (statusCard) {
    statusCard.outerHTML = renderStatusCard();
  }
};

const render = () => {
  appElement.innerHTML = `
    <main class="shell">
      <section class="hero">
        <div class="hero__content">
          <p class="eyebrow">Первая версия</p>
          <h1>Кроссплатформенное desktop-приложение</h1>
          <p class="hero__text">
            Современный интерфейс для Windows 10 и ALT Linux с локальным режимом и
            многопользовательской работой через сетевой ресурс.
          </p>
          <div class="hero__actions" aria-label="Выбор режима работы">
            <button class="mode-button ${state.mode === 'local' ? 'mode-button--active' : ''}" data-mode="local">
              Локальный режим
            </button>
            <button class="mode-button ${state.mode === 'network' ? 'mode-button--active' : ''}" data-mode="network">
              Сетевой режим
            </button>
          </div>
        </div>
        ${renderStatusCard()}
      </section>

      <section class="panel">
        <div>
          <p class="section-label">Ресурс</p>
          <h2>Размещение данных</h2>
          <p>
            Для многопользовательского режима укажите общий сетевой путь, например
            <span class="inline-code">\\\\server\\share</span>,
            <span class="inline-code">smb://server/share</span> или
            <span class="inline-code">/mnt/share</span>.
          </p>
        </div>
        <label class="network-field">
          <span>Сетевой ресурс</span>
          <input
            type="text"
            value="${escapeHtml(state.networkResourcePath)}"
            placeholder="Введите путь к сетевому ресурсу"
            ${state.mode === 'local' ? 'disabled' : ''}
            data-network-path
          />
        </label>
      </section>

      <section class="grid">
        <article class="panel">
          <p class="section-label">Платформы</p>
          <h2>Поддерживаемый запуск</h2>
          <div class="platform-list">
            ${supportedPlatforms
              .map(
                (platform) => `
                  <div class="platform-card">
                    <span class="platform-card__icon">✓</span>
                    <div>
                      <strong>${escapeHtml(platform.name)}</strong>
                      <p>${escapeHtml(platform.description)}</p>
                    </div>
                  </div>
                `,
              )
              .join('')}
          </div>
        </article>

        <article class="panel">
          <p class="section-label">Разработка</p>
          <h2>Основные этапы</h2>
          <ol class="stage-list">
            ${developmentStages.map((stage) => `<li>${escapeHtml(stage)}</li>`).join('')}
          </ol>
        </article>
      </section>
    </main>
  `;

  appElement.querySelectorAll<HTMLButtonElement>('[data-mode]').forEach((button) => {
    button.addEventListener('click', () => {
      state = setWorkMode(state, button.dataset.mode as WorkMode);
      render();
    });
  });

  appElement.querySelector<HTMLInputElement>('[data-network-path]')?.addEventListener('input', (event) => {
    state = setNetworkResourcePath(state, (event.target as HTMLInputElement).value);
    refreshStatusCard();
  });
};

render();
