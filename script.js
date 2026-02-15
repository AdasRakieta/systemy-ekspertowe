// Konfiguracja API
const API_URL = 'http://localhost:5001';

// Stan aplikacji (single select wszedzie)
const appState = {
    selectedOptions: {
        gatunek: null,
        klimat: null,
        tempo: null,
        dlugosc: null,
        swiat: null,
        wiek_bohatera: null,
        miejsce: null,
        pochodzenie: null
    }
};

// Mapowanie polskich nazw
const polishLabels = {
    gatunek: {
        fantasy: 'Fantasy',
        kryminal: 'Kryminał',
        romans: 'Romans',
        biografia: 'Biografia',
        science_fiction: 'Science Fiction',
        historyczna: 'Historyczna',
        thriller: 'Thriller',
        podroznicza: 'Podróżnicza',
        obyczajowa: 'Obyczajowa',
        horror: 'Horror',
        mlodziezowa: 'Młodzieżowa',
        esej: 'Esej',
        reportaz: 'Reportaż',
        przygodowa: 'Przygodowa',
        satyra: 'Satyra',
        postapo: 'Postapokaliptyczna',
        detektywistyczna: 'Detektywistyczna',
        fakt: 'Literatura faktu',
        groza: 'Groza',
        komiks: 'Komiks',
        poezja: 'Poezja'
    },
    klimat: {
        mroczny: 'Mroczny',
        lekki: 'Lekki',
        inspirujacy: 'Inspirujący',
        refleksyjny: 'Refleksyjny',
        epicki: 'Epicki',
        psychologiczny: 'Psychologiczny',
        przygodowy: 'Przygodowy',
        realistyczny: 'Realistyczny',
        gotycki: 'Gotycki',
        humorystyczny: 'Humorystyczny',
        tajemniczy: 'Tajemniczy',
        dynamiczny: 'Dynamiczny',
        liryczny: 'Liryczny',
        relaksujacy: 'Relaksujący'
    },
    dlugosc: {
        krotka: 'Krótka',
        srednia: 'Średnia',
        dluga: 'Długa',
        bardzo_dluga: 'Bardzo długa'
    },
    tempo: {
        wolne: 'Wolne',
        umiarkowane: 'Umiarkowane',
        dynamiczne: 'Dynamiczne'
    },
    wiek_bohatera: {
        mlody: 'Młody',
        dorosly: 'Dorosły',
        starszy: 'Starszy',
        brak: 'Brak bohatera'
    },
    swiat: {
        magiczny: 'Magiczny',
        przyszlosc: 'Przyszłość',
        wspolczesny: 'Współczesny',
        historyczny: 'Historyczny'
    },
    miejsce: {
        miasto: 'Miasto',
        wies: 'Wieś',
        swiat: 'Świat',
        las: 'Las',
        zamek: 'Zamek',
        szkola: 'Szkoła',
        dzungla: 'Dżungla',
        europa: 'Europa'
    },
    pochodzenie: {
        skandynawia: 'Skandynawia',
        europa: 'Europa',
        azja: 'Azja'
    }
};

const suggestionValueMap = {
    tempo: {
        powolne: 'wolne'
    }
};

// Presety (gotowe profile) - single select
const presets = [
    {
        name: '🧙 Fan Fantasy',
        icon: '🧙',
        selections: {
            gatunek: 'fantasy',
            klimat: 'epicki',
            tempo: 'dynamiczne',
            swiat: 'magiczny'
        }
    },
    {
        name: '🔍 Detektyw',
        icon: '🔍',
        selections: {
            gatunek: 'kryminal',
            klimat: 'tajemniczy',
            tempo: 'dynamiczne'
        }
    },
    {
        name: '😌 Lektura relaksująca',
        icon: '😌',
        selections: {
            gatunek: 'romans',
            klimat: 'lekki',
            tempo: 'wolne'
        }
    },
    {
        name: '🚀 Sci-Fi',
        icon: '🚀',
        selections: {
            gatunek: 'science_fiction',
            klimat: 'dynamiczny',
            tempo: 'dynamiczne',
            swiat: 'przyszlosc'
        }
    },
    {
        name: '💭 Głębokie przemyślenia',
        icon: '💭',
        selections: {
            gatunek: 'biografia',
            klimat: 'refleksyjny',
            tempo: 'wolne'
        }
    },
    {
        name: '😱 Mroczne klimaty',
        icon: '😱',
        selections: {
            gatunek: 'horror',
            klimat: 'mroczny',
            tempo: 'dynamiczne'
        }
    }
];

// Inicjalizacja aplikacji
document.addEventListener('DOMContentLoaded', () => {
    loadOptions();
    loadSuggestions();
    setupFormHandlers();
    setupAdvancedToggle();
    renderPresets();
});

function renderPresets() {
    const grid = document.getElementById('presetsGrid');
    if (!grid) return;

    grid.innerHTML = '';
    presets.forEach(preset => {
        const card = document.createElement('div');
        card.className = 'preset-card';
        card.innerHTML = `
            <div class="preset-icon">${preset.icon}</div>
            <div class="preset-name">${preset.name}</div>
        `;
        card.addEventListener('click', () => applyPreset(preset));
        grid.appendChild(card);
    });
}

function applyPreset(preset) {
    resetSelections();

    Object.entries(preset.selections).forEach(([field, value]) => {
        appState.selectedOptions[field] = value;
    });

    refreshAllChips();
    updateSelectionSummary();

    const hasAdvanced = preset.selections.swiat || preset.selections.dlugosc ||
        preset.selections.wiek_bohatera || preset.selections.miejsce ||
        preset.selections.pochodzenie;

    if (hasAdvanced) {
        const advancedOptions = document.getElementById('advancedOptions');
        const icon = document.querySelector('.toggle-icon');
        if (advancedOptions) advancedOptions.style.display = 'block';
        if (icon) icon.textContent = '▲';
    }

    const formContainer = document.querySelector('.form-container');
    if (formContainer) {
        formContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function resetSelections() {
    appState.selectedOptions = {
        gatunek: null,
        klimat: null,
        tempo: null,
        dlugosc: null,
        swiat: null,
        wiek_bohatera: null,
        miejsce: null,
        pochodzenie: null
    };
}

function setupAdvancedToggle() {
    const toggleBtn = document.getElementById('toggleAdvanced');
    const advancedOptions = document.getElementById('advancedOptions');
    const icon = toggleBtn ? toggleBtn.querySelector('.toggle-icon') : null;

    if (!toggleBtn || !advancedOptions) return;

    toggleBtn.addEventListener('click', () => {
        const isHidden = advancedOptions.style.display === 'none';
        advancedOptions.style.display = isHidden ? 'block' : 'none';
        if (icon) icon.textContent = isHidden ? '▲' : '▼';
    });
}

async function loadOptions() {
    try {
        const response = await fetch(`${API_URL}/api/options`);
        const options = await response.json();

        const allFields = [
            'gatunek', 'klimat', 'tempo', 'dlugosc', 'swiat',
            'wiek_bohatera', 'miejsce', 'pochodzenie'
        ];

        allFields.forEach(field => {
            renderChips(field, options[field]);
        });
    } catch (error) {
        console.error('Błąd ładowania opcji:', error);
        showError('Nie można załadować opcji formularza. Sprawdź czy serwer jest uruchomiony.');
    }
}

async function loadSuggestions() {
    try {
        const response = await fetch(`${API_URL}/api/suggestions`);
        if (!response.ok) {
            throw new Error('Błąd ładowania sugestii');
        }
        const suggestions = await response.json();
        renderSuggestions(suggestions);
    } catch (error) {
        console.error('Błąd ładowania sugestii:', error);
        const section = document.getElementById('suggestionsSection');
        if (section) section.style.display = 'none';
    }
}

function renderSuggestions(data) {
    const section = document.getElementById('suggestionsSection');
    const grid = document.getElementById('suggestionsGrid');
    const meta = document.getElementById('suggestionsMeta');
    if (!section || !grid) return;

    const items = [
        { label: 'Sugerowany gatunek na teraz', value: data.gatunek, field: 'gatunek' },
        { label: 'Świat na tę porę roku', value: data.swiat, field: 'swiat' },
        { label: 'Klimat przy dobrym nastroju', value: data.klimat_dobry_nastroj, field: 'klimat' },
        { label: 'Klimat przy złym nastroju', value: data.klimat_zly_nastroj, field: 'klimat' },
        { label: 'Tempo przy małej ilości czasu', value: data.tempo_malo_czasu, field: 'tempo' },
        { label: 'Tempo przy dużej ilości czasu', value: data.tempo_duzo_czasu, field: 'tempo' }
    ];

    grid.innerHTML = '';
    items.forEach(item => {
        const applyValue = mapSuggestionValue(item.field, item.value);
        const labelValue = getLabel(item.field, applyValue || item.value);
        const card = document.createElement('div');
        card.className = 'suggestion-card';
        card.innerHTML = `
            <div class="suggestion-label">${item.label}</div>
            <div class="suggestion-value">${labelValue}</div>
            <button class="suggestion-apply" type="button" ${applyValue ? '' : 'disabled'}>
                Ustaw w formularzu
            </button>
        `;

        const btn = card.querySelector('.suggestion-apply');
        if (btn && applyValue) {
            btn.addEventListener('click', () => applySuggestion(item.field, applyValue));
        }

        grid.appendChild(card);
    });

    if (meta) {
        const hour = typeof data.godzina === 'number' ? `${data.godzina}:00` : '-';
        const month = typeof data.miesiac === 'number' ? data.miesiac : '-';
        meta.textContent = `Aktualna godzina: ${hour} • Miesiąc: ${month}`;
    }

    section.style.display = 'block';
}

function renderChips(field, values) {
    const container = document.getElementById(`${field}Chips`);
    if (!container || !Array.isArray(values)) return;

    container.innerHTML = '';
    values.forEach(value => {
        const chip = document.createElement('button');
        chip.type = 'button';
        chip.className = 'chip';
        chip.textContent = polishLabels[field]?.[value] || value;
        chip.dataset.field = field;
        chip.dataset.value = value;

        if (appState.selectedOptions[field] === value) {
            chip.classList.add('selected');
        }

        chip.addEventListener('click', () => {
            toggleChip(field, value);
        });

        container.appendChild(chip);
    });

    updateBadge(field);
}

function toggleChip(field, value) {
    if (appState.selectedOptions[field] === value) {
        appState.selectedOptions[field] = null;
    } else {
        appState.selectedOptions[field] = value;
    }

    refreshChips(field);
    updateBadge(field);
    updateSelectionSummary();
}

function refreshChips(field) {
    const container = document.getElementById(`${field}Chips`);
    if (!container) return;

    const chips = container.querySelectorAll('.chip');
    chips.forEach(chip => {
        const value = chip.dataset.value;
        chip.classList.toggle('selected', appState.selectedOptions[field] === value);
    });
}

function refreshAllChips() {
    const allFields = [
        'gatunek', 'klimat', 'tempo', 'dlugosc', 'swiat',
        'wiek_bohatera', 'miejsce', 'pochodzenie'
    ];

    allFields.forEach(field => refreshChips(field));
    allFields.forEach(updateBadge);
}

function updateBadge(field) {
    const badge = document.getElementById(`${field}Badge`);
    if (!badge) return;

    const selection = appState.selectedOptions[field];
    if (selection) {
        badge.textContent = polishLabels[field]?.[selection] || selection;
        badge.className = 'badge badge-active';
    } else {
        badge.textContent = 'Nieważne';
        badge.className = 'badge';
    }
}

function updateSelectionSummary() {
    const summary = document.getElementById('selectionSummary');
    const content = document.getElementById('summaryContent');
    if (!summary || !content) return;

    const allSelections = [];
    Object.entries(appState.selectedOptions).forEach(([field, value]) => {
        if (value) {
            allSelections.push(polishLabels[field]?.[value] || value);
        }
    });

    if (allSelections.length > 0) {
        content.innerHTML = allSelections.map(sel =>
            `<span class="summary-tag">${sel}</span>`
        ).join('');
        summary.style.display = 'block';
    } else {
        summary.style.display = 'none';
    }
}

function getLabel(field, value) {
    if (!value) return '-';
    return polishLabels[field]?.[value] || value;
}

function mapSuggestionValue(field, value) {
    const mapped = suggestionValueMap[field]?.[value] || value;
    const hasLabel = Boolean(polishLabels[field]?.[mapped]);
    return hasLabel ? mapped : null;
}

function applySuggestion(field, value) {
    appState.selectedOptions[field] = value;
    refreshChips(field);
    updateBadge(field);
    updateSelectionSummary();

    const needsAdvanced = ['dlugosc', 'swiat', 'wiek_bohatera', 'miejsce', 'pochodzenie'];
    if (needsAdvanced.includes(field)) {
        const advancedOptions = document.getElementById('advancedOptions');
        const icon = document.querySelector('.toggle-icon');
        if (advancedOptions) advancedOptions.style.display = 'block';
        if (icon) icon.textContent = '▲';
    }
}

function setupFormHandlers() {
    const form = document.getElementById('preferencesForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await getRecommendations();
    });

    form.addEventListener('reset', () => {
        resetSelections();
        refreshAllChips();
        updateSelectionSummary();
        hideResults();
        hideError();
    });
}

async function getRecommendations() {
    const preferences = {};

    Object.entries(appState.selectedOptions).forEach(([field, value]) => {
        if (value) {
            preferences[field] = value;
        }
    });

    if (Object.keys(preferences).length === 0) {
        showError('Wybierz przynajmniej jedną preferencję!');
        return;
    }

    showLoading();
    hideError();
    hideResults();

    try {
        const response = await fetch(`${API_URL}/api/recommend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(preferences)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Błąd serwera');
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Błąd:', error);
        showError(`Błąd: ${error.message}. Sprawdź czy serwer Flask jest uruchomiony.`);
    } finally {
        hideLoading();
    }
}

function displayResults(data) {
    const top3Div = document.getElementById('top3');
    const explanationsDiv = document.getElementById('explanations');

    if (!top3Div || !explanationsDiv) return;

    top3Div.innerHTML = '';
    explanationsDiv.innerHTML = '';

    const medals = ['🥇', '🥈', '🥉'];
    data.top3.forEach((book, index) => {
        const card = createBookCard(book, index, medals[index]);
        top3Div.appendChild(card);
    });

    if (data.winners && data.winners.length > 0) {
        data.winners.forEach(winner => {
            const explanation = createExplanation(winner);
            explanationsDiv.appendChild(explanation);
        });
    }

    showResults();
}

function createBookCard(book, index, medal) {
    const card = document.createElement('div');
    card.className = `book-card medal-${index + 1}`;

    if (book.score === 100) {
        card.classList.add('winner');
    }

    const scorePercentage = book.score;
    card.innerHTML = `
        <div class="book-title">
            <span class="medal">${medal}</span>
            <span>${book.name}</span>
        </div>
        <div class="book-score">${book.score} pkt</div>
        <div class="score-bar">
            <div class="score-fill" style="width: ${scorePercentage}%"></div>
        </div>
        <div class="reasons-count">
            ${book.reasons.length} spełnionych kryteriów
        </div>
    `;

    return card;
}

function createExplanation(book) {
    const section = document.createElement('div');
    section.className = 'explanation-section';

    const title = document.createElement('h3');
    title.className = 'explanation-title';
    title.textContent = `Wyjaśnienie dla: ${book.name}`;

    const list = document.createElement('ul');
    list.className = 'reason-list';

    book.reasons.forEach(reason => {
        const item = document.createElement('li');
        item.className = 'reason-item';
        item.textContent = reason;
        list.appendChild(item);
    });

    section.appendChild(title);
    section.appendChild(list);

    return section;
}

function showLoading() {
    const el = document.getElementById('loading');
    if (el) el.style.display = 'block';
}

function hideLoading() {
    const el = document.getElementById('loading');
    if (el) el.style.display = 'none';
}

function showResults() {
    const el = document.getElementById('results');
    if (el) {
        el.style.display = 'block';
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function hideResults() {
    const el = document.getElementById('results');
    if (el) el.style.display = 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    if (!errorDiv) return;
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function hideError() {
    const errorDiv = document.getElementById('error');
    if (errorDiv) errorDiv.style.display = 'none';
}
