// Konfiguracja API
const API_URL = 'http://localhost:5001';

// Mapowanie polskich nazw dla wartości
const polishLabels = {
    gatunek: {
        'fantasy': 'Fantasy',
        'kryminal': 'Kryminał',
        'romans': 'Romans',
        'biografia': 'Biografia',
        'science_fiction': 'Science Fiction',
        'historyczna': 'Historyczna',
        'thriller': 'Thriller',
        'podroznicza': 'Podróżnicza',
        'obyczajowa': 'Obyczajowa',
        'horror': 'Horror',
        'mlodziezowa': 'Młodzieżowa',
        'esej': 'Esej',
        'reportaz': 'Reportaż',
        'przygodowa': 'Przygodowa',
        'satyra': 'Satyra',
        'postapo': 'Postapokaliptyczna',
        'detektywistyczna': 'Detektywistyczna',
        'fakt': 'Literatura faktu',
        'groza': 'Groza',
        'komiks': 'Komiks',
        'poezja': 'Poezja'
    },
    klimat: {
        'mroczny': 'Mroczny',
        'lekki': 'Lekki',
        'inspirujacy': 'Inspirujący',
        'refleksyjny': 'Refleksyjny',
        'epicki': 'Epicki',
        'psychologiczny': 'Psychologiczny',
        'przygodowy': 'Przygodowy',
        'realistyczny': 'Realistyczny',
        'gotycki': 'Gotycki',
        'humorystyczny': 'Humorystyczny',
        'tajemniczy': 'Tajemniczy',
        'dynamiczny': 'Dynamiczny',
        'liryczny': 'Liryczny'
    },
    dlugosc: {
        'krotka': 'Krótka',
        'srednia': 'Średnia',
        'dluga': 'Długa',
        'bardzo_dluga': 'Bardzo długa'
    },
    tempo: {
        'wolne': 'Wolne',
        'umiarkowane': 'Umiarkowane',
        'dynamiczne': 'Dynamiczne'
    },
    wiek_bohatera: {
        'mlody': 'Młody',
        'dorosly': 'Dorosły',
        'starszy': 'Starszy',
        'brak': 'Brak bohatera'
    },
    swiat: {
        'magiczny': 'Magiczny',
        'przyszlosc': 'Przyszłość',
        'wspolczesny': 'Współczesny'
    },
    miejsce: {
        'miasto': 'Miasto',
        'wies': 'Wieś',
        'swiat': 'Świat',
        'las': 'Las',
        'zamek': 'Zamek',
        'szkola': 'Szkoła',
        'dzungla': 'Dżungla',
        'europa': 'Europa'
    },
    pochodzenie: {
        'skandynawia': 'Skandynawia',
        'europa': 'Europa',
        'azja': 'Azja'
    },
    epoka: {
        'sredniowiecze': 'Średniowiecze',
        'wspolczesna': 'Współczesna',
        'przyszlosc': 'Przyszłość'
    }
};

// Inicjalizacja aplikacji
document.addEventListener('DOMContentLoaded', () => {
    loadOptions();
    setupFormHandlers();
});

// Ładowanie opcji do formularza
async function loadOptions() {
    try {
        const response = await fetch(`${API_URL}/api/options`);
        const options = await response.json();

        // Wypełnianie selectów
        for (const [field, values] of Object.entries(options)) {
            const select = document.getElementById(field);
            if (select) {
                values.forEach(value => {
                    const option = document.createElement('option');
                    option.value = value;
                    option.textContent = polishLabels[field]?.[value] || value;
                    select.appendChild(option);
                });
            }
        }
    } catch (error) {
        console.error('Błąd ładowania opcji:', error);
        showError('Nie można załadować opcji formularza. Sprawdź czy serwer jest uruchomiony.');
    }
}

// Obsługa formularza
function setupFormHandlers() {
    const form = document.getElementById('preferencesForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await getRecommendations();
    });

    form.addEventListener('reset', () => {
        hideResults();
        hideError();
    });
}

// Pobieranie rekomendacji
async function getRecommendations() {
    const form = document.getElementById('preferencesForm');
    const formData = new FormData(form);
    const preferences = {};

    // Konwersja FormData do obiektu
    for (const [key, value] of formData.entries()) {
        if (value) {
            preferences[key] = value;
        }
    }

    // Sprawdzanie czy użytkownik wybrał jakieś preferencje
    if (Object.keys(preferences).length === 0) {
        showError('Wybierz przynajmniej jedną preferencję!');
        return;
    }

    // Pokazywanie loadera
    showLoading();
    hideError();
    hideResults();

    try {
        const response = await fetch(`${API_URL}/api/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
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

// Wyświetlanie wyników
function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    const top3Div = document.getElementById('top3');
    const explanationsDiv = document.getElementById('explanations');

    // Czyszczenie poprzednich wyników
    top3Div.innerHTML = '';
    explanationsDiv.innerHTML = '';

    // TOP 3
    const medals = ['🥇', '🥈', '🥉'];
    data.top3.forEach((book, index) => {
        const card = createBookCard(book, index, medals[index]);
        top3Div.appendChild(card);
    });

    // Wyjaśnienia dla zwycięzców
    if (data.winners && data.winners.length > 0) {
        data.winners.forEach(winner => {
            const explanation = createExplanation(winner);
            explanationsDiv.appendChild(explanation);
        });
    }

    // Pokazywanie wyników
    showResults();
}

// Tworzenie karty książki
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

// Tworzenie sekcji wyjaśnień
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

// Funkcje pomocnicze do pokazywania/ukrywania elementów
function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showResults() {
    document.getElementById('results').style.display = 'block';
    // Płynne przewijanie do wyników
    document.getElementById('results').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

function hideResults() {
    document.getElementById('results').style.display = 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

function hideError() {
    document.getElementById('error').style.display = 'none';
}
