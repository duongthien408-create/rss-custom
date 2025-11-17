// Supabase Configuration
const SUPABASE_URL = 'https://aiorbvjphoslukcqvawx.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFpb3JidmpwaG9zbHVrY3F2YXd4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI2MDAyMzAsImV4cCI6MjA3ODE3NjIzMH0.02hPReDUSObXlzgSJJW77jVAfw4EymyW9wZfaOW0N00';

// Initialize Supabase client
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Global state
let allArticles = [];
let filteredArticles = [];

// DOM Elements
const loadingState = document.getElementById('loadingState');
const articlesGrid = document.getElementById('articlesGrid');
const emptyState = document.getElementById('emptyState');
const errorState = document.getElementById('errorState');
const errorMessage = document.getElementById('errorMessage');
const searchInput = document.getElementById('searchInput');
const sortSelect = document.getElementById('sortSelect');
const refreshBtn = document.getElementById('refreshBtn');

// Load articles on page load
document.addEventListener('DOMContentLoaded', () => {
    loadArticles();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    searchInput.addEventListener('input', debounce(handleSearch, 300));
    sortSelect.addEventListener('change', handleSort);
    refreshBtn.addEventListener('click', loadArticles);
}

// Load articles from Supabase
async function loadArticles() {
    try {
        showLoading();

        const { data, error } = await supabase
            .from('trendforce_news')
            .select('*')
            .order('date', { ascending: false })
            .limit(100);

        if (error) throw error;

        allArticles = data || [];
        filteredArticles = [...allArticles];

        updateStats();
        renderArticles();
        updateLastUpdate();

        hideLoading();

    } catch (error) {
        console.error('Error loading articles:', error);
        showError(error.message);
    }
}

// Render articles to the grid
function renderArticles() {
    if (filteredArticles.length === 0) {
        showEmpty();
        return;
    }

    articlesGrid.innerHTML = filteredArticles.map(article => createArticleCard(article)).join('');
    articlesGrid.classList.remove('hidden');
    emptyState.classList.add('hidden');
}

// Create article card HTML
function createArticleCard(article) {
    const date = formatDate(article.date);

    // Ưu tiên hiển thị tiếng Việt, fallback sang tiếng Anh
    const title = article.title_vi || article.title;
    const summary = article.summary_vi || article.summary || 'No summary available';
    const truncatedSummary = truncateText(summary, 150);
    const category = article.category || 'Uncategorized';

    // Hiển thị badge nếu có bản dịch tiếng Việt
    const hasVietnamese = article.title_vi || article.summary_vi;

    return `
        <article class="bg-white rounded-lg shadow card-hover overflow-hidden">
            ${article.thumbnail ? `
                <img src="${article.thumbnail}" alt="${title}" class="w-full h-48 object-cover" onerror="this.style.display='none'">
            ` : ''}

            <div class="p-6">
                <div class="flex items-center gap-2 mb-3">
                    <span class="badge bg-blue-100 text-primary">
                        📰 ${category}
                    </span>
                    ${hasVietnamese ? `
                        <span class="badge bg-green-100 text-green-700">
                            🇻🇳 Tiếng Việt
                        </span>
                    ` : ''}
                    <span class="text-sm text-gray-500">
                        ${date}
                    </span>
                </div>

                <h2 class="text-xl font-semibold text-gray-900 mb-3 line-clamp-2 hover:text-primary transition">
                    <a href="${article.url}" target="_blank" rel="noopener noreferrer">
                        ${title}
                    </a>
                </h2>

                ${summary !== 'No summary available' ? `
                    <p class="text-gray-600 mb-4 line-clamp-3">
                        ${truncatedSummary}
                    </p>
                ` : ''}

                <a
                    href="${article.url}"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="inline-flex items-center text-primary hover:text-blue-700 font-medium"
                >
                    Read more
                    <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                </a>
            </div>
        </article>
    `;
}

// Handle search
function handleSearch(e) {
    const query = e.target.value.toLowerCase().trim();

    if (!query) {
        filteredArticles = [...allArticles];
    } else {
        filteredArticles = allArticles.filter(article =>
            article.title.toLowerCase().includes(query) ||
            (article.title_vi && article.title_vi.toLowerCase().includes(query)) ||
            (article.summary && article.summary.toLowerCase().includes(query)) ||
            (article.summary_vi && article.summary_vi.toLowerCase().includes(query))
        );
    }

    renderArticles();
}

// Handle sort
function handleSort(e) {
    const sortBy = e.target.value;

    switch (sortBy) {
        case 'date_desc':
            filteredArticles.sort((a, b) => new Date(b.date) - new Date(a.date));
            break;
        case 'date_asc':
            filteredArticles.sort((a, b) => new Date(a.date) - new Date(b.date));
            break;
        case 'title':
            filteredArticles.sort((a, b) => a.title.localeCompare(b.title));
            break;
    }

    renderArticles();
}

// Update statistics
function updateStats() {
    const total = allArticles.length;
    const today = allArticles.filter(a => isToday(a.date)).length;
    const thisWeek = allArticles.filter(a => isThisWeek(a.date)).length;
    const categories = new Set(allArticles.map(a => a.category).filter(Boolean)).size;

    document.getElementById('totalArticles').textContent = total;
    document.getElementById('todayArticles').textContent = today;
    document.getElementById('weekArticles').textContent = thisWeek;
    document.getElementById('categories').textContent = categories || 'N/A';
}

// Update last update time
function updateLastUpdate() {
    const now = new Date();
    const formatted = now.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    document.getElementById('lastUpdate').textContent = formatted;
}

// Utility functions
function formatDate(dateString) {
    if (!dateString) return 'No date';

    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;

    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });
}

function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength).trim() + '...';
}

function isToday(dateString) {
    if (!dateString) return false;
    const date = new Date(dateString);
    const today = new Date();
    return date.toDateString() === today.toDateString();
}

function isThisWeek(dateString) {
    if (!dateString) return false;
    const date = new Date(dateString);
    const now = new Date();
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    return date >= weekAgo && date <= now;
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// UI state functions
function showLoading() {
    loadingState.classList.remove('hidden');
    articlesGrid.classList.add('hidden');
    emptyState.classList.add('hidden');
    errorState.classList.add('hidden');
}

function hideLoading() {
    loadingState.classList.add('hidden');
}

function showEmpty() {
    articlesGrid.classList.add('hidden');
    emptyState.classList.remove('hidden');
    errorState.classList.add('hidden');
}

function showError(message) {
    loadingState.classList.add('hidden');
    articlesGrid.classList.add('hidden');
    emptyState.classList.add('hidden');
    errorState.classList.remove('hidden');
    errorMessage.textContent = message;
}
