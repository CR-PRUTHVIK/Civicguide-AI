/**
 * CivicGuide AI Portal - Client-Side Interactive Scripts
 * Features:
 * 1. AI Citizen Assistant Chatbot (Homepage & Floating Drawer)
 * 2. English & Hindi Bilingual Language Guidance
 * 3. Verified Official Government Source Attribution
 * 4. Step-by-Step Eligibility Wizard (Triggered from Top Right)
 * 5. State-Wise Welfares and Scholarships Filter
 */

// Global Language State ('en' | 'hi')
let currentLang = localStorage.getItem('gov_portal_lang') || 'en';

// Translations Dictionary
const I18N = {
  en: {
    portalTitle: "CivicGuide AI",
    govSubtitle: "Government of India Citizen Services Directory",
    officialRepo: "Official Information & Guidelines Repository",
    textSize: "Text Size:",
    contrast: "Contrast",
    antiFraud: "Anti-Fraud Guide",
    navHome: "Home",
    navScholarships: "Scholarships (NSP)",
    navCaste: "Caste Certificate",
    navVoter: "Voter Services (ECI)",
    navCivic: "Civic & Municipal",
    navSelectState: "Select State",
    navChecklist: "Doc Checklist",
    navFaqs: "Grievance & FAQs",
    checkEligibilityBtnTop: "🎯 Check Eligibility",
    searchPlaceholder: "Search schemes, Form 6, Caste SC/OBC, DL, Domicile, States, Exams...",
    officialSourceLabel: "🏛️ Verified Official Source:",
    selectStatePrompt: "Select Your State for State-Specific Welfares & Scholarships:",
    stateWelfareTitle: "State Government Welfare Schemes & Subsidies",
    stateScholarshipTitle: "State-Specific Scholarship Schemes",
    officialApplyBtn: "Apply on Official Portal ↗",
    verifiedBadge: "Official Govt Source"
  },
  hi: {
    portalTitle: "सिविकगाइड AI",
    govSubtitle: "भारत सरकार नागरिक सेवा निर्देशिका",
    officialRepo: "आधिकारिक सूचना एवं दिशा-निर्देश रिपॉजिटरी",
    textSize: "फ़ॉन्ट आकार:",
    contrast: "कंट्रास्ट",
    antiFraud: "धोखाधड़ी से सुरक्षा गाइड",
    navHome: "होम",
    navScholarships: "छात्रवृत्ति (NSP)",
    navCaste: "जाति प्रमाण पत्र",
    navVoter: "मतदाता सेवाएं (ECI)",
    navCivic: "नागरिक सेवाएं",
    navSelectState: "राज्य चुनें",
    navChecklist: "दस्तावेज चेकलिस्ट",
    navFaqs: "शिकायत एवं FAQs",
    checkEligibilityBtnTop: "🎯 पात्रता जांचें",
    searchPlaceholder: "योजनाएं, फॉर्म 6, जाति SC/OBC, ड्राइविंग लाइसेंस, राज्य, परीक्षाएं खोजें...",
    officialSourceLabel: "🏛️ सत्यापित आधिकारिक सरकारी स्रोत:",
    selectStatePrompt: "राज्य-विशिष्ट कल्याणकारी योजनाओं एवं छात्रवृत्ति हेतु अपना राज्य चुनें:",
    stateWelfareTitle: "राज्य सरकार की प्रमुख कल्याणकारी योजनाएं एवं सहायता",
    stateScholarshipTitle: "राज्य-विशिष्ट छात्रवृत्ति योजनाएं",
    officialApplyBtn: "आधिकारिक पोर्टल पर आवेदन करें ↗",
    verifiedBadge: "सत्यापित आधिकारिक स्रोत"
  }
};

// Accessibility: Font Size Scaler
let currentFontSize = 100;
function changeFontSize(delta) {
  if (delta === 0) {
    currentFontSize = 100;
  } else {
    currentFontSize = Math.min(130, Math.max(85, currentFontSize + delta * 10));
  }
  document.documentElement.style.fontSize = currentFontSize + "%";
}

// Accessibility: Contrast Mode
function toggleContrast() {
  document.body.classList.toggle('high-contrast');
  const isHigh = document.body.classList.contains('high-contrast');
  localStorage.setItem('gov_portal_contrast', isHigh ? 'high' : 'normal');
}

// Language Toggle
function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem('gov_portal_lang', lang);
  applyTranslations();
  updateWizardLanguage();
}

function toggleLanguage() {
  setLanguage(currentLang === 'en' ? 'hi' : 'en');
}

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (I18N[currentLang] && I18N[currentLang][key]) {
      el.textContent = I18N[currentLang][key];
    }
  });

  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (I18N[currentLang] && I18N[currentLang][key]) {
      el.placeholder = I18N[currentLang][key];
    }
  });

  const langToggleBtn = document.getElementById('lang-toggle-btn');
  if (langToggleBtn) {
    langToggleBtn.innerHTML = currentLang === 'en' 
      ? `<span class="font-bold text-amber-300">EN</span> / हिंदी` 
      : `EN / <span class="font-bold text-amber-300">हिंदी</span>`;
  }

  // Toggle bilingual content blocks
  document.querySelectorAll('.lang-en').forEach(el => {
    el.style.display = currentLang === 'en' ? '' : 'none';
  });
  document.querySelectorAll('.lang-hi').forEach(el => {
    el.style.display = currentLang === 'hi' ? '' : 'none';
  });
}

// Restore saved preferences on load
document.addEventListener('DOMContentLoaded', () => {
  if (localStorage.getItem('gov_portal_contrast') === 'high') {
    document.body.classList.add('high-contrast');
  }
  applyTranslations();
  initGlobalSearch();
  initChecklistTracker();
});

// Live Global Search with Debounce
function initGlobalSearch() {
  const searchInput = document.getElementById('global-search-input');
  const searchResults = document.getElementById('search-dropdown-results');
  if (!searchInput || !searchResults) return;

  let debounceTimer;

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    clearTimeout(debounceTimer);

    if (query.length < 2) {
      searchResults.classList.add('hidden');
      searchResults.innerHTML = '';
      return;
    }

    debounceTimer = setTimeout(async () => {
      try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const data = await res.json();
        renderSearchResults(data, searchResults);
      } catch (err) {
        console.error('Search fetch error:', err);
      }
    }, 250);
  });

  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
      searchResults.classList.add('hidden');
    }
  });
}

function renderSearchResults(data, container) {
  if (!data || data.total_results === 0) {
    container.innerHTML = `
      <div class="p-4 text-center text-sm text-slate-500">
        ${currentLang === 'hi' 
          ? `कोई परिणाम नहीं मिला "<strong>${escapeHtml(data.query)}</strong>"। कृपया UPSC, Form 6, NSP, OBC, Domicile या राज्य का नाम खोजें।`
          : `No exact matches found for "<strong>${escapeHtml(data.query)}</strong>". Try searching for <em>UPSC</em>, <em>Form 6</em>, <em>NSP</em>, <em>OBC</em>, <em>Domicile</em>, or your state name.`}
      </div>
    `;
    container.classList.remove('hidden');
    return;
  }

  let html = `<div class="p-2 border-b border-slate-100 text-xs font-semibold text-slate-500 uppercase tracking-wider">${currentLang === 'hi' ? `कुल ${data.total_results} परिणाम मिले` : `Found ${data.total_results} results`}</div>`;
  html += `<div class="max-h-96 overflow-y-auto divide-y divide-slate-100">`;

  // Exams
  if (data.results.exams && data.results.exams.length > 0) {
    html += `<div class="p-2 bg-slate-50 text-xs font-bold text-indigo-900 flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-indigo-600"></span> ${currentLang === 'hi' ? 'प्रतियोगी परीक्षाएं' : 'Competitive Exams'} (${data.results.exams.length})</div>`;
    data.results.exams.forEach(item => {
      html += `
        <a href="${item.url}" class="block p-3 hover:bg-indigo-50/50 transition">
          <div class="flex items-center justify-between gap-2">
            <span class="font-medium text-sm text-slate-900">${escapeHtml(item.title)}</span>
            <span class="text-xs bg-indigo-100 text-indigo-800 px-2 py-0.5 rounded font-medium">${escapeHtml(item.badge)}</span>
          </div>
          <p class="text-xs text-slate-600 mt-1 line-clamp-1">${escapeHtml(item.description)}</p>
        </a>
      `;
    });
  }

  // Scholarships
  if (data.results.scholarships && data.results.scholarships.length > 0) {
    html += `<div class="p-2 bg-slate-50 text-xs font-bold text-blue-900 flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-blue-600"></span> ${currentLang === 'hi' ? 'छात्रवृत्ति' : 'Scholarships'} (${data.results.scholarships.length})</div>`;
    data.results.scholarships.forEach(item => {
      html += `
        <a href="${item.url}" class="block p-3 hover:bg-blue-50/50 transition">
          <div class="flex items-center justify-between gap-2">
            <span class="font-medium text-sm text-slate-900">${escapeHtml(item.title)}</span>
            <span class="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded font-medium">${escapeHtml(item.badge)}</span>
          </div>
          <p class="text-xs text-slate-600 mt-1 line-clamp-1">${escapeHtml(item.description)}</p>
        </a>
      `;
    });
  }

  // Welfares
  if (data.results.welfares && data.results.welfares.length > 0) {
    html += `<div class="p-2 bg-slate-50 text-xs font-bold text-rose-900 flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-rose-600"></span> ${currentLang === 'hi' ? 'कल्याणकारी योजनाएं' : 'Welfare Schemes'} (${data.results.welfares.length})</div>`;
    data.results.welfares.forEach(item => {
      html += `
        <a href="${item.url}" class="block p-3 hover:bg-rose-50/50 transition">
          <div class="flex items-center justify-between gap-2">
            <span class="font-medium text-sm text-slate-900">${escapeHtml(item.title)}</span>
            <span class="text-xs bg-rose-100 text-rose-800 px-2 py-0.5 rounded font-medium">${escapeHtml(item.badge)}</span>
          </div>
          <p class="text-xs text-slate-600 mt-1 line-clamp-1">${escapeHtml(item.description)}</p>
        </a>
      `;
    });
  }

  // Voter Forms
  if (data.results.voter_forms && data.results.voter_forms.length > 0) {
    html += `<div class="p-2 bg-slate-50 text-xs font-bold text-orange-900 flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-orange-600"></span> ${currentLang === 'hi' ? 'मतदाता सेवाएं' : 'Voter Services'} (${data.results.voter_forms.length})</div>`;
    data.results.voter_forms.forEach(item => {
      html += `
        <a href="${item.url}" class="block p-3 hover:bg-orange-50/50 transition">
          <div class="flex items-center justify-between gap-2">
            <span class="font-medium text-sm text-slate-900">${escapeHtml(item.title)}</span>
            <span class="text-xs bg-orange-100 text-orange-800 px-2 py-0.5 rounded font-medium">${escapeHtml(item.badge)}</span>
          </div>
          <p class="text-xs text-slate-600 mt-1 line-clamp-1">${escapeHtml(item.description)}</p>
        </a>
      `;
    });
  }

  // Caste Categories
  if (data.results.caste_categories && data.results.caste_categories.length > 0) {
    html += `<div class="p-2 bg-slate-50 text-xs font-bold text-purple-900 flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-purple-600"></span> ${currentLang === 'hi' ? 'जाति प्रमाण पत्र' : 'Caste Certificate'} (${data.results.caste_categories.length})</div>`;
    data.results.caste_categories.forEach(item => {
      html += `
        <a href="${item.url}" class="block p-3 hover:bg-purple-50/50 transition">
          <div class="flex items-center justify-between gap-2">
            <span class="font-medium text-sm text-slate-900">${escapeHtml(item.title)}</span>
            <span class="text-xs bg-purple-100 text-purple-800 px-2 py-0.5 rounded font-medium">${escapeHtml(item.badge)}</span>
          </div>
          <p class="text-xs text-slate-600 mt-1 line-clamp-1">${escapeHtml(item.description)}</p>
        </a>
      `;
    });
  }

  // Civic Services
  if (data.results.civic_services && data.results.civic_services.length > 0) {
    html += `<div class="p-2 bg-slate-50 text-xs font-bold text-emerald-900 flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-600"></span> ${currentLang === 'hi' ? 'नागरिक सेवाएं' : 'Civic Services'} (${data.results.civic_services.length})</div>`;
    data.results.civic_services.forEach(item => {
      html += `
        <a href="${item.url}" class="block p-3 hover:bg-emerald-50/50 transition">
          <div class="flex items-center justify-between gap-2">
            <span class="font-medium text-sm text-slate-900">${escapeHtml(item.title)}</span>
            <span class="text-xs bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded font-medium">${escapeHtml(item.badge)}</span>
          </div>
          <p class="text-xs text-slate-600 mt-1 line-clamp-1">${escapeHtml(item.description)}</p>
        </a>
      `;
    });
  }

  // State Portals
  if (data.results.state_portals && data.results.state_portals.length > 0) {
    html += `<div class="p-2 bg-slate-50 text-xs font-bold text-slate-900 flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-slate-600"></span> ${currentLang === 'hi' ? 'राज्य पोर्टल' : 'State Portals'} (${data.results.state_portals.length})</div>`;
    data.results.state_portals.forEach(item => {
      html += `
        <a href="${item.url}" class="block p-3 hover:bg-slate-100 transition">
          <div class="flex items-center justify-between gap-2">
            <span class="font-medium text-sm text-slate-900">${escapeHtml(item.title)}</span>
            <span class="text-xs bg-slate-200 text-slate-800 px-2 py-0.5 rounded font-medium">${escapeHtml(item.badge)}</span>
          </div>
          <p class="text-xs text-slate-600 mt-1 line-clamp-1">${escapeHtml(item.description)}</p>
        </a>
      `;
    });
  }

  html += `</div>`;
  container.innerHTML = html;
  container.classList.remove('hidden');
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

function formatChatAnswer(text) {
  if (!text) return '';
  // Convert markdown bold and bullets to html
  let formatted = escapeHtml(text);
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
  formatted = formatted.replace(/`([^`]+)`/g, '<code class="bg-slate-100 px-1 py-0.5 rounded font-mono text-blue-900">$1</code>');
  formatted = formatted.replace(/\n\n/g, '<br><br>');
  formatted = formatted.replace(/\n- /g, '<br>&bull; ');
  formatted = formatted.replace(/\n/g, '<br>');
  return formatted;
}

// Checklist progress tracker
function initChecklistTracker() {
  const checkboxes = document.querySelectorAll('.checklist-checkbox');
  if (checkboxes.length === 0) return;

  function updateProgress() {
    const total = checkboxes.length;
    const checked = document.querySelectorAll('.checklist-checkbox:checked').length;
    const percentage = total > 0 ? Math.round((checked / total) * 100) : 0;

    const bar = document.getElementById('checklist-progress-bar');
    const label = document.getElementById('checklist-progress-text');
    if (bar) bar.style.width = `${percentage}%`;
    if (label) label.textContent = currentLang === 'hi' 
      ? `${total} में से ${checked} दस्तावेज तैयार (${percentage}%)`
      : `${checked} of ${total} documents ready (${percentage}%)`;
  }

  checkboxes.forEach(cb => {
    cb.addEventListener('change', updateProgress);
  });

  updateProgress();
}


/* =========================================================================
   AI CITIZEN ASSISTANT CHATBOT LOGIC
   ========================================================================= */

function toggleFloatingChatbot() {
  const drawer = document.getElementById('floating-chatbot-drawer');
  if (!drawer) return;
  drawer.classList.toggle('hidden');
  if (!drawer.classList.contains('hidden')) {
    const input = document.getElementById('drawer-chat-input');
    if (input) input.focus();
  }
}

async function handleDrawerChatSubmit(e) {
  e.preventDefault();
  const input = document.getElementById('drawer-chat-input');
  const messagesContainer = document.getElementById('drawer-chat-messages');
  if (!input || !messagesContainer) return;

  const userQuery = input.value.trim();
  if (!userQuery) return;

  // Add User Message Bubble
  messagesContainer.innerHTML += `
    <div class="flex justify-end">
      <div class="bg-blue-900 text-white p-3 rounded-2xl max-w-[85%] leading-relaxed shadow-sm">
        ${escapeHtml(userQuery)}
      </div>
    </div>
  `;
  input.value = '';
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  // Typing Indicator
  const typingId = 'typing-' + Date.now();
  messagesContainer.innerHTML += `
    <div id="${typingId}" class="bg-white p-3 rounded-2xl border border-slate-200 shadow-sm max-w-[85%] text-slate-500 italic">
      CivicGuide AI is researching official guidelines...
    </div>
  `;
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userQuery, lang: currentLang })
    });
    const data = await res.json();

    const typingEl = document.getElementById(typingId);
    if (typingEl) typingEl.remove();

    let linksHtml = '';
    if (data.suggested_links && data.suggested_links.length > 0) {
      linksHtml = `<div class="mt-2 pt-2 border-t border-slate-100 flex flex-wrap gap-1.5">`;
      data.suggested_links.forEach(l => {
        linksHtml += `<a href="${l.url}" target="_blank" rel="noopener noreferrer" class="text-[10px] bg-blue-50 text-blue-900 px-2 py-1 rounded font-semibold hover:bg-blue-100 transition">${escapeHtml(l.label)} ↗</a>`;
      });
      linksHtml += `</div>`;
    }

    messagesContainer.innerHTML += `
      <div class="bg-white p-3.5 rounded-2xl border border-slate-200 shadow-sm max-w-[90%] text-slate-800 leading-relaxed">
        <div class="font-bold text-xs text-blue-900 mb-1 flex items-center justify-between">
          <span>${escapeHtml(data.title)}</span>
          <span class="text-[10px] text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded font-medium">Verified Govt Data</span>
        </div>
        <div class="text-xs text-slate-700 leading-relaxed">${formatChatAnswer(data.answer)}</div>
        <div class="mt-2 text-[10px] text-slate-400">🏛️ <em>Source: ${escapeHtml(data.official_source)}</em></div>
        ${linksHtml}
      </div>
    `;
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    lucide.createIcons();
  } catch (err) {
    const typingEl = document.getElementById(typingId);
    if (typingEl) typingEl.remove();
    messagesContainer.innerHTML += `<div class="bg-rose-50 text-rose-700 p-2.5 rounded-xl text-xs">Error fetching response. Please try again.</div>`;
  }
}

// Homepage Interactive Chatbot Handler
async function handleHomeChatSubmit(e) {
  e.preventDefault();
  const input = document.getElementById('home-chat-input');
  const messagesContainer = document.getElementById('home-chat-messages');
  if (!input || !messagesContainer) return;

  const userQuery = input.value.trim();
  if (!userQuery) return;

  // Render user message
  messagesContainer.innerHTML += `
    <div class="flex justify-end">
      <div class="bg-blue-900 text-white p-3.5 rounded-2xl max-w-[85%] leading-relaxed shadow-sm text-xs sm:text-sm">
        ${escapeHtml(userQuery)}
      </div>
    </div>
  `;
  input.value = '';
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  // Typing
  const typingId = 'home-typing-' + Date.now();
  messagesContainer.innerHTML += `
    <div id="${typingId}" class="bg-slate-50 p-3.5 rounded-2xl border border-slate-200 text-xs text-slate-500 italic max-w-[80%]">
      CivicGuide AI is consulting official gazettes and statutory guidelines...
    </div>
  `;
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userQuery, lang: currentLang })
    });
    const data = await res.json();

    const typingEl = document.getElementById(typingId);
    if (typingEl) typingEl.remove();

    let linksHtml = '';
    if (data.suggested_links && data.suggested_links.length > 0) {
      linksHtml = `<div class="mt-3 pt-3 border-t border-slate-100 flex flex-wrap gap-2">`;
      data.suggested_links.forEach(l => {
        linksHtml += `<a href="${l.url}" ${l.url.startsWith('http') ? 'target="_blank" rel="noopener noreferrer"' : ''} class="text-xs bg-blue-50 hover:bg-blue-100 text-blue-900 font-bold px-3 py-1.5 rounded-xl transition border border-blue-200 inline-flex items-center gap-1">${escapeHtml(l.label)} ↗</a>`;
      });
      linksHtml += `</div>`;
    }

    messagesContainer.innerHTML += `
      <div class="bg-slate-50 p-4 sm:p-5 rounded-2xl border border-slate-200 shadow-sm max-w-[95%] text-slate-800">
        <div class="flex items-center justify-between gap-2 mb-2 pb-2 border-b border-slate-200">
          <div class="font-bold text-sm text-blue-950 font-serif flex items-center gap-1.5">
            <i data-lucide="sparkles" class="w-4 h-4 text-amber-500"></i>
            <span>${escapeHtml(data.title)}</span>
          </div>
          <span class="text-[11px] font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-md">Official Gov Verified</span>
        </div>
        <div class="text-xs sm:text-sm text-slate-700 leading-relaxed">${formatChatAnswer(data.answer)}</div>
        <div class="mt-3 text-[11px] text-slate-500 bg-white p-2 rounded-xl border border-slate-200">
          🏛️ <strong>Verified Source:</strong> ${escapeHtml(data.official_source)}
        </div>
        ${linksHtml}
      </div>
    `;
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    lucide.createIcons();
  } catch (err) {
    const typingEl = document.getElementById(typingId);
    if (typingEl) typingEl.remove();
    messagesContainer.innerHTML += `<div class="bg-rose-50 text-rose-700 p-3 rounded-xl text-xs">Failed to fetch response. Please try again.</div>`;
  }
}

function askHomeQuickPrompt(promptText) {
  const input = document.getElementById('home-chat-input');
  if (input) {
    input.value = promptText;
    document.getElementById('home-chat-form').dispatchEvent(new Event('submit'));
  }
}


/* =========================================================================
   ELIGIBILITY WIZARD MODAL & LOGIC
   ========================================================================= */

let wizardStep = 1;
const totalWizardSteps = 6;
const wizardAnswers = {
  age: '',
  education: '',
  category: '',
  income: '',
  gender_status: '',
  state: ''
};

function openEligibilityWizard() {
  const modal = document.getElementById('eligibility-wizard-modal');
  if (!modal) return;
  modal.classList.remove('hidden');
  document.body.classList.add('overflow-hidden');
  wizardStep = 1;
  renderWizardStep();
}

function closeEligibilityWizard() {
  const modal = document.getElementById('eligibility-wizard-modal');
  if (!modal) return;
  modal.classList.add('hidden');
  document.body.classList.remove('overflow-hidden');
}

function nextWizardStep(answerKey, answerValue) {
  wizardAnswers[answerKey] = answerValue;
  if (wizardStep < totalWizardSteps) {
    wizardStep++;
    renderWizardStep();
  } else {
    calculateAndShowWizardResults();
  }
}

function prevWizardStep() {
  if (wizardStep > 1) {
    wizardStep--;
    renderWizardStep();
  }
}

function updateWizardLanguage() {
  const modal = document.getElementById('eligibility-wizard-modal');
  if (modal && !modal.classList.contains('hidden')) {
    renderWizardStep();
  }
}

function renderWizardStep() {
  const container = document.getElementById('wizard-step-content');
  const progressText = document.getElementById('wizard-progress-text');
  const progressBar = document.getElementById('wizard-progress-bar');
  const backBtn = document.getElementById('wizard-back-btn');

  if (!container) return;

  const pct = Math.round(((wizardStep - 1) / totalWizardSteps) * 100);
  if (progressBar) progressBar.style.width = `${pct}%`;
  if (progressText) {
    progressText.textContent = currentLang === 'hi' 
      ? `चरण ${wizardStep} / ${totalWizardSteps}` 
      : `Step ${wizardStep} of ${totalWizardSteps}`;
  }

  if (backBtn) {
    backBtn.style.display = wizardStep === 1 ? 'none' : 'inline-flex';
  }

  let html = '';

  if (wizardStep === 1) {
    html = `
      <div class="text-center mb-6">
        <span class="inline-block text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-full mb-2">
          ${currentLang === 'hi' ? 'आयु निर्धारण' : 'Age Verification'}
        </span>
        <h3 class="text-xl sm:text-2xl font-black text-slate-900 font-serif">
          ${currentLang === 'hi' ? 'आपकी वर्तमान आयु (उम्र) कितनी है?' : 'What is your current age?'}
        </h3>
        <p class="text-xs sm:text-sm text-slate-500 mt-1">
          ${currentLang === 'hi' ? 'आयु के आधार पर मतदाता पंजीकरण, छात्रवृत्ति व ड्राइविंग लाइसेंस की पात्रता निर्धारित होती है।' : 'Age determines voter registration, scholarship limits, and driving license eligibility.'}
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-xl mx-auto">
        <button onclick="nextWizardStep('age', 'below-18')" class="p-4 bg-slate-50 hover:bg-blue-50 border-2 border-slate-200 hover:border-blue-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-blue-900">${currentLang === 'hi' ? '18 वर्ष से कम (नाबालिग)' : 'Below 18 Years'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'स्कूली छात्र / प्री-मैट्रिक छात्रवृत्ति' : 'School student / Pre-Matric schemes'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-blue-600"></i>
        </button>

        <button onclick="nextWizardStep('age', '18-25')" class="p-4 bg-slate-50 hover:bg-blue-50 border-2 border-slate-200 hover:border-blue-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-blue-900">${currentLang === 'hi' ? '18 से 25 वर्ष' : '18 to 25 Years'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'कॉलेज / उच्च शिक्षा / वोटर फॉर्म 6 / DL' : 'College / Higher education / Voter Form 6 / DL'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-blue-600"></i>
        </button>

        <button onclick="nextWizardStep('age', '26-40')" class="p-4 bg-slate-50 hover:bg-blue-50 border-2 border-slate-200 hover:border-blue-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-blue-900">${currentLang === 'hi' ? '26 से 40 वर्ष' : '26 to 40 Years'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'उच्च शोध / स्वरोजगार / नागरिक कल्याण' : 'Higher research / Self-employment / Civic services'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-blue-600"></i>
        </button>

        <button onclick="nextWizardStep('age', 'above-40')" class="p-4 bg-slate-50 hover:bg-blue-50 border-2 border-slate-200 hover:border-blue-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-blue-900">${currentLang === 'hi' ? '40 वर्ष से अधिक' : 'Above 40 Years'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'नागरिक प्रमाण पत्र / पेंशन / राशन कार्ड' : 'Certificates / Pensions / Ration Card'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-blue-600"></i>
        </button>
      </div>
    `;
  } else if (wizardStep === 2) {
    html = `
      <div class="text-center mb-6">
        <span class="inline-block text-xs font-bold text-purple-600 bg-purple-50 px-3 py-1 rounded-full mb-2">
          ${currentLang === 'hi' ? 'शैक्षणिक योग्यता' : 'Education Status'}
        </span>
        <h3 class="text-xl sm:text-2xl font-black text-slate-900 font-serif">
          ${currentLang === 'hi' ? 'आपकी वर्तमान शैक्षणिक योग्यता या कोर्स क्या है?' : 'What is your current educational status?'}
        </h3>
        <p class="text-xs sm:text-sm text-slate-500 mt-1">
          ${currentLang === 'hi' ? 'नेशनल स्कॉलरशिप पोर्टल (NSP) एवं राज्य छात्रवृत्ति हेतु शैक्षणिक स्तर आवश्यक है।' : 'Required for National Scholarship Portal (NSP) & state education grants.'}
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-xl mx-auto">
        <button onclick="nextWizardStep('education', 'Class 9-10')" class="p-4 bg-slate-50 hover:bg-purple-50 border-2 border-slate-200 hover:border-purple-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-purple-900">${currentLang === 'hi' ? 'कक्षा 9 - 10 (माध्यमिक)' : 'Class 9 - 10 (Pre-Matric)'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'प्री-मैट्रिक छात्रवृत्ति' : 'Pre-Matric Schemes'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-purple-600"></i>
        </button>

        <button onclick="nextWizardStep('education', 'Class 11-12')" class="p-4 bg-slate-50 hover:bg-purple-50 border-2 border-slate-200 hover:border-purple-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-purple-900">${currentLang === 'hi' ? 'कक्षा 11 - 12 (उच्च माध्यमिक)' : 'Class 11 - 12 (Higher Secondary)'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'पोस्ट-मैट्रिक / पीएम-यशस्वी' : 'Post-Matric / PM-YASASVI'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-purple-600"></i>
        </button>

        <button onclick="nextWizardStep('education', 'Graduation')" class="p-4 bg-slate-50 hover:bg-purple-50 border-2 border-slate-200 hover:border-purple-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-purple-900">${currentLang === 'hi' ? 'स्नातक / डिग्री (B.Tech, B.Sc, BA, MBBS)' : 'Graduation / Degree (B.Tech, B.Sc, BA, MBBS)'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'CSSS / AICTE प्रगति / पोस्ट-मैट्रिक' : 'CSSS / AICTE Pragati / Post-Matric'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-purple-600"></i>
        </button>

        <button onclick="nextWizardStep('education', 'Post-Graduation')" class="p-4 bg-slate-50 hover:bg-purple-50 border-2 border-slate-200 hover:border-purple-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-purple-900">${currentLang === 'hi' ? 'स्नातकोत्तर (M.Tech, M.Sc, MA, PhD)' : 'Post-Graduation / PhD (M.Tech, M.Sc, MA)'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'उच्च शोध अनुदान / DST INSPIRE' : 'Research grants / DST INSPIRE'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-purple-600"></i>
        </button>

        <button onclick="nextWizardStep('education', 'Diploma')" class="p-4 bg-slate-50 hover:bg-purple-50 border-2 border-slate-200 hover:border-purple-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-purple-900">${currentLang === 'hi' ? 'पॉलिटेक्निक / डिप्लोमा' : 'Polytechnic / Diploma'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'तकनीकी छात्रवृत्ति' : 'Technical scholarships'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-purple-600"></i>
        </button>

        <button onclick="nextWizardStep('education', 'Non-Student')" class="p-4 bg-slate-50 hover:bg-purple-50 border-2 border-slate-200 hover:border-purple-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-purple-900">${currentLang === 'hi' ? 'वर्तमान में छात्र नहीं (Non-Student)' : 'Not currently studying (Non-Student)'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'नागरिक सेवाएं, जाति, राशन व वोटर कार्ड' : 'Civic, Caste, Ration & Voter services'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-purple-600"></i>
        </button>
      </div>
    `;
  } else if (wizardStep === 3) {
    html = `
      <div class="text-center mb-6">
        <span class="inline-block text-xs font-bold text-amber-600 bg-amber-50 px-3 py-1 rounded-full mb-2">
          ${currentLang === 'hi' ? 'सामाजिक श्रेणी' : 'Social Category'}
        </span>
        <h3 class="text-xl sm:text-2xl font-black text-slate-900 font-serif">
          ${currentLang === 'hi' ? 'आपका सामाजिक वर्ग (Category) क्या है?' : 'What is your social category?'}
        </h3>
        <p class="text-xs sm:text-sm text-slate-500 mt-1">
          ${currentLang === 'hi' ? 'संवैधानिक आरक्षण व विशेष कल्याणकारी योजनाओं हेतु सही वर्ग चुनें।' : 'Select to find caste certificate formats and category quota benefits.'}
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-xl mx-auto">
        <button onclick="nextWizardStep('category', 'SC')" class="p-4 bg-slate-50 hover:bg-amber-50 border-2 border-slate-200 hover:border-amber-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-amber-900">${currentLang === 'hi' ? 'अनुसूचित जाति (SC)' : 'Scheduled Caste (SC)'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'अनुच्छेद 341 / आजीवन वैधता' : 'Article 341 / Lifetime validity'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-amber-600"></i>
        </button>

        <button onclick="nextWizardStep('category', 'ST')" class="p-4 bg-slate-50 hover:bg-amber-50 border-2 border-slate-200 hover:border-amber-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-amber-900">${currentLang === 'hi' ? 'अनुसूचित जनजाति (ST)' : 'Scheduled Tribe (ST)'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'अनुच्छेद 342 / जनजातीय कल्याण' : 'Article 342 / Tribal welfare'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-amber-600"></i>
        </button>

        <button onclick="nextWizardStep('category', 'OBC')" class="p-4 bg-slate-50 hover:bg-amber-50 border-2 border-slate-200 hover:border-amber-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-amber-900">${currentLang === 'hi' ? 'अन्य पिछड़ा वर्ग (OBC - Non-Creamy)' : 'OBC (Non-Creamy Layer)'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'आय सीमा ₹8 लाख / 1 वर्ष वैधता' : 'Income < ₹8L / 1-year validity'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-amber-600"></i>
        </button>

        <button onclick="nextWizardStep('category', 'EWS')" class="p-4 bg-slate-50 hover:bg-amber-50 border-2 border-slate-200 hover:border-amber-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-amber-900">${currentLang === 'hi' ? 'आर्थिक कमजोर वर्ग (EWS)' : 'Economically Weaker Section (EWS)'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? '103वां संविधान संशोधन / 10% कोटा' : '103rd Amendment / 10% Quota'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-amber-600"></i>
        </button>

        <button onclick="nextWizardStep('category', 'Minority')" class="p-4 bg-slate-50 hover:bg-amber-50 border-2 border-slate-200 hover:border-amber-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-amber-900">${currentLang === 'hi' ? 'अल्पसंख्यक (Muslim, Sikh, Christian, Jain, etc.)' : 'Minority Community'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'अल्पसंख्यक कार्य मंत्रालय योजनाएं' : 'Ministry of Minority Affairs schemes'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-amber-600"></i>
        </button>

        <button onclick="nextWizardStep('category', 'General')" class="p-4 bg-slate-50 hover:bg-amber-50 border-2 border-slate-200 hover:border-amber-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-amber-900">${currentLang === 'hi' ? 'सामान्य / अनारक्षित (General/Open)' : 'General / Unreserved'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'मेरिट आधारित व राज्य कल्याण योजनाएं' : 'Merit & General state schemes'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-amber-600"></i>
        </button>
      </div>
    `;
  } else if (wizardStep === 4) {
    html = `
      <div class="text-center mb-6">
        <span class="inline-block text-xs font-bold text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full mb-2">
          ${currentLang === 'hi' ? 'पारिवारिक आय' : 'Family Annual Income'}
        </span>
        <h3 class="text-xl sm:text-2xl font-black text-slate-900 font-serif">
          ${currentLang === 'hi' ? 'आपके परिवार की कुल वार्षिक आय कितनी है?' : 'What is your gross annual family income?'}
        </h3>
        <p class="text-xs sm:text-sm text-slate-500 mt-1">
          ${currentLang === 'hi' ? 'समस्त स्रोतों (वेतन, कृषि, व्यापार आदि) से कुल वार्षिक आय।' : 'Total combined annual income from all sources.'}
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-xl mx-auto">
        <button onclick="nextWizardStep('income', '250000')" class="p-4 bg-slate-50 hover:bg-emerald-50 border-2 border-slate-200 hover:border-emerald-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-emerald-900">${currentLang === 'hi' ? '₹2.50 लाख तक / वर्ष' : 'Up to ₹2,50,000 / year'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'SC/ST/OBC पोस्ट-मैट्रिक पूर्ण छात्रवृत्ति हेतु पात्र' : 'Eligible for 100% Post-Matric schemes'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-emerald-600"></i>
        </button>

        <button onclick="nextWizardStep('income', '450000')" class="p-4 bg-slate-50 hover:bg-emerald-50 border-2 border-slate-200 hover:border-emerald-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-emerald-900">${currentLang === 'hi' ? '₹2.50 लाख से ₹4.50 लाख / वर्ष' : '₹2.5 Lakhs to ₹4.5 Lakhs'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'केंद्रीय क्षेत्र (CSSS) छात्रवृत्ति हेतु पात्र' : 'Eligible for CSSS Central Sector scheme'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-emerald-600"></i>
        </button>

        <button onclick="nextWizardStep('income', '800000')" class="p-4 bg-slate-50 hover:bg-emerald-50 border-2 border-slate-200 hover:border-emerald-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-emerald-900">${currentLang === 'hi' ? '₹4.50 लाख से ₹8.00 लाख / वर्ष' : '₹4.5 Lakhs to ₹8.0 Lakhs'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'OBC-NCL, EWS एवं AICTE प्रगति पात्र' : 'OBC-NCL, EWS & AICTE Pragati eligible'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-emerald-600"></i>
        </button>

        <button onclick="nextWizardStep('income', '9999999')" class="p-4 bg-slate-50 hover:bg-emerald-50 border-2 border-slate-200 hover:border-emerald-500 rounded-2xl text-left transition flex items-center justify-between group">
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-emerald-900">${currentLang === 'hi' ? '₹8.00 लाख से अधिक / वर्ष' : 'Above ₹8.0 Lakhs / year'}</div>
            <div class="text-xs text-slate-500">${currentLang === 'hi' ? 'DST INSPIRE व मेरिट आधारित योजनाएं' : 'DST INSPIRE & General merit schemes'}</div>
          </div>
          <i data-lucide="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-emerald-600"></i>
        </button>
      </div>
    `;
  } else if (wizardStep === 5) {
    html = `
      <div class="text-center mb-6">
        <span class="inline-block text-xs font-bold text-rose-600 bg-rose-50 px-3 py-1 rounded-full mb-2">
          ${currentLang === 'hi' ? 'लिंग / विशेष दर्जा' : 'Gender & Special Status'}
        </span>
        <h3 class="text-xl sm:text-2xl font-black text-slate-900 font-serif">
          ${currentLang === 'hi' ? 'आपका लिंग एवं विशेष स्थिति क्या है?' : 'What is your gender & special status?'}
        </h3>
        <p class="text-xs sm:text-sm text-slate-500 mt-1">
          ${currentLang === 'hi' ? 'बालिकाओं एवं दिव्यांगजनों हेतु कई विशेष सरकारी छात्रवृत्तियां उपलब्ध हैं।' : 'Unlock dedicated grants for female students and specially-abled citizens.'}
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 max-w-xl mx-auto">
        <button onclick="nextWizardStep('gender_status', 'Female')" class="p-4 bg-slate-50 hover:bg-rose-50 border-2 border-slate-200 hover:border-rose-500 rounded-2xl text-left transition flex flex-col justify-between group">
          <div class="w-10 h-10 rounded-xl bg-rose-100 text-rose-700 flex items-center justify-center font-bold mb-3">
            <i data-lucide="user" class="w-5 h-5"></i>
          </div>
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-rose-900">${currentLang === 'hi' ? 'महिला / छात्रा' : 'Female (Girl Student)'}</div>
            <div class="text-xs text-slate-500 mt-0.5">${currentLang === 'hi' ? 'AICTE प्रगति, बेगम हज़रत महल, लाड़ली बहना आदि' : 'AICTE Pragati, Begum Hazrat, Ladki Bahin, etc.'}</div>
          </div>
        </button>

        <button onclick="nextWizardStep('gender_status', 'PwD')" class="p-4 bg-slate-50 hover:bg-rose-50 border-2 border-slate-200 hover:border-rose-500 rounded-2xl text-left transition flex flex-col justify-between group">
          <div class="w-10 h-10 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center font-bold mb-3">
            <i data-lucide="accessibility" class="w-5 h-5"></i>
          </div>
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-rose-900">${currentLang === 'hi' ? 'दिव्यांगजन (PwD >= 40%)' : 'Specially-Abled (PwD >= 40%)'}</div>
            <div class="text-xs text-slate-500 mt-0.5">${currentLang === 'hi' ? 'AICTE सक्षम, विशेष सहायक अनुदान' : 'AICTE Saksham, UDID benefits'}</div>
          </div>
        </button>

        <button onclick="nextWizardStep('gender_status', 'Male')" class="p-4 bg-slate-50 hover:bg-rose-50 border-2 border-slate-200 hover:border-rose-500 rounded-2xl text-left transition flex flex-col justify-between group">
          <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center font-bold mb-3">
            <i data-lucide="user-check" class="w-5 h-5"></i>
          </div>
          <div>
            <div class="font-bold text-sm text-slate-900 group-hover:text-rose-900">${currentLang === 'hi' ? 'पुरुष / सामान्य आवेदक' : 'Male / General Applicant'}</div>
            <div class="text-xs text-slate-500 mt-0.5">${currentLang === 'hi' ? 'केंद्रीय एवं राज्य सामान्य योजनाएं' : 'Standard Central & State schemes'}</div>
          </div>
        </button>
      </div>
    `;
  } else if (wizardStep === 6) {
    html = `
      <div class="text-center mb-6">
        <span class="inline-block text-xs font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full mb-2">
          ${currentLang === 'hi' ? 'राज्य चयन' : 'State / UT Residence'}
        </span>
        <h3 class="text-xl sm:text-2xl font-black text-slate-900 font-serif">
          ${currentLang === 'hi' ? 'आप किस राज्य / केंद्र शासित प्रदेश के निवासी हैं?' : 'Which State / UT are you a resident of?'}
        </h3>
        <p class="text-xs sm:text-sm text-slate-500 mt-1">
          ${currentLang === 'hi' ? 'आपके राज्य की विशिष्ट कल्याणकारी योजनाएं एवं छात्रवृत्ति प्रदर्शित की जाएंगी।' : 'Loads specific state government welfares, scholarships & e-district services.'}
        </p>
      </div>

      <div class="max-w-md mx-auto space-y-4">
        <div>
          <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
            ${currentLang === 'hi' ? 'राज्य या केंद्र शासित प्रदेश चुनें' : 'Select State or Union Territory'}
          </label>
          <select id="wizard-state-select" class="w-full bg-slate-50 border-2 border-slate-300 rounded-2xl px-4 py-3 text-sm font-semibold focus:border-indigo-600 focus:outline-none">
            <option value="maharashtra">Maharashtra (महाराष्ट्र)</option>
            <option value="uttar-pradesh">Uttar Pradesh (उत्तर प्रदेश)</option>
            <option value="bihar">Bihar (बिहार)</option>
            <option value="karnataka">Karnataka (कर्नाटक)</option>
            <option value="tamil-nadu">Tamil Nadu (तमिलनाडु)</option>
            <option value="west-bengal">West Bengal (पश्चिम बंगाल)</option>
            <option value="rajasthan">Rajasthan (राजस्थान)</option>
            <option value="gujarat">Gujarat (गुजरात)</option>
            <option value="madhya-pradesh">Madhya Pradesh (मध्य प्रदेश)</option>
            <option value="delhi">Delhi (दिल्ली)</option>
            <option value="andhra-pradesh">Andhra Pradesh (आंध्र प्रदेश)</option>
            <option value="telangana">Telangana (तेलंगाना)</option>
            <option value="kerala">Kerala (केरल)</option>
            <option value="punjab">Punjab (पंजाब)</option>
            <option value="haryana">Haryana (हरियाणा)</option>
            <option value="odisha">Odisha (ओडिशा)</option>
            <option value="assam">Assam (असम)</option>
            <option value="jharkhand">Jharkhand (झारखंड)</option>
            <option value="chhattisgarh">Chhattisgarh (छत्तीसगढ़)</option>
            <option value="uttarakhand">Uttarakhand (उत्तराखंड)</option>
            <option value="himachal-pradesh">Himachal Pradesh (हिमाचल प्रदेश)</option>
            <option value="goa">Goa (गोवा)</option>
          </select>
        </div>

        <button onclick="finishWizard()" class="w-full bg-indigo-900 hover:bg-indigo-800 text-white font-bold py-3 px-6 rounded-2xl text-sm transition shadow-lg flex items-center justify-center gap-2">
          <i data-lucide="sparkles" class="w-4 h-4 text-amber-300"></i>
          <span>${currentLang === 'hi' ? 'पात्रता परिणाम देखें →' : 'View My Eligibility Results →'}</span>
        </button>
      </div>
    `;
  }

  container.innerHTML = html;
  lucide.createIcons();
}

function finishWizard() {
  const stateSelect = document.getElementById('wizard-state-select');
  if (stateSelect) {
    wizardAnswers.state = stateSelect.value;
  }
  calculateAndShowWizardResults();
}

async function calculateAndShowWizardResults() {
  const container = document.getElementById('wizard-step-content');
  const progressText = document.getElementById('wizard-progress-text');
  const progressBar = document.getElementById('wizard-progress-bar');
  const backBtn = document.getElementById('wizard-back-btn');

  if (progressBar) progressBar.style.width = '100%';
  if (progressText) {
    progressText.textContent = currentLang === 'hi' ? 'विश्लेषण पूर्ण' : 'Analysis Complete';
  }
  if (backBtn) backBtn.style.display = 'none';

  container.innerHTML = `<div class="text-center py-12 text-slate-500 font-medium">${currentLang === 'hi' ? 'आपकी पात्रता का विश्लेषण किया जा रहा है...' : 'Analyzing your eligibility...'}</div>`;

  try {
    const res = await fetch(`/api/check-full-eligibility`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(wizardAnswers)
    });
    const data = await res.json();
    renderWizardResults(data, container);
  } catch (err) {
    console.error('Eligibility calculation error:', err);
    container.innerHTML = `<div class="text-center text-rose-600 py-8">Failed to calculate results. Please try again.</div>`;
  }
}

function renderWizardResults(data, container) {
  const isHi = currentLang === 'hi';
  let html = `
    <div class="mb-6 pb-4 border-b border-slate-200 flex items-center justify-between">
      <div>
        <span class="text-xs font-bold text-emerald-800 bg-emerald-100 px-3 py-1 rounded-full">
          ${isHi ? '✓ पात्रता परिणाम' : '✓ Eligibility Results Ready'}
        </span>
        <h3 class="text-xl font-black text-slate-900 mt-1 font-serif">
          ${isHi ? 'आपके लिए अनुशंसित सरकारी योजनाएं एवं सेवाएं' : 'Recommended Government Schemes & Entitlements'}
        </h3>
      </div>
      <button onclick="openEligibilityWizard()" class="text-xs text-blue-900 font-bold hover:underline">
        ${isHi ? 'पुनः जांचें ↺' : 'Retake Quiz ↺'}
      </button>
    </div>

    <!-- Official Verified Source Alert -->
    <div class="bg-blue-50 border border-blue-200 rounded-2xl p-4 text-xs text-blue-950 mb-6 flex items-start gap-2.5">
      <i data-lucide="shield-check" class="w-4 h-4 text-blue-700 flex-shrink-0 mt-0.5"></i>
      <div>
        <strong>${isHi ? 'आधिकारिक स्रोत आश्वासन:' : 'Official Source Assurance:'}</strong>
        ${isHi ? 'नीचे दी गई समस्त योजनाएं एवं आवेदन लिंक संबंधित केंद्र एवं राज्य मंत्रालयों के आधिकारिक .gov.in पोर्टल्स से सत्यापित हैं।' : 'All matching schemes and application links below are verified directly from official .gov.in central and state ministry portals.'}
      </div>
    </div>
  `;

  // 1. Central Scholarships Match
  html += `
    <div class="mb-6">
      <h4 class="text-sm font-bold text-slate-900 uppercase tracking-wider mb-3 flex items-center gap-1.5">
        <i data-lucide="graduation-cap" class="w-4 h-4 text-amber-600"></i>
        <span>${isHi ? 'पात्र केंद्रीय छात्रवृत्तियां (NSP / AICTE / DST)' : 'Eligible Central Scholarships (NSP / AICTE)'}</span>
      </h4>
  `;

  if (data.central_scholarships && data.central_scholarships.length > 0) {
    html += `<div class="space-y-3">`;
    data.central_scholarships.forEach(s => {
      html += `
        <div class="bg-slate-50 p-4 rounded-2xl border border-slate-200 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between gap-2 mb-1">
              <span class="text-xs font-bold text-amber-900 bg-amber-100 px-2 py-0.5 rounded">${escapeHtml(isHi ? (s.category_hi || s.category) : s.category)}</span>
              <span class="text-[11px] text-slate-500 font-medium">${escapeHtml(s.ministry)}</span>
            </div>
            <h5 class="font-bold text-sm text-slate-900">${escapeHtml(isHi ? (s.title_hi || s.title) : s.title)}</h5>
            <p class="text-xs text-slate-600 mt-1">${escapeHtml(isHi ? (s.benefits_hi || s.benefits) : s.benefits)}</p>
          </div>
          <div class="pt-3 mt-3 border-t border-slate-200 flex items-center justify-between">
            <span class="text-[11px] text-slate-500">${isHi ? 'स्रोत:' : 'Source:'} <strong>${escapeHtml(s.portal_name)}</strong></span>
            <a href="${s.portal_url}" target="_blank" rel="noopener noreferrer" class="text-xs font-bold text-white bg-blue-900 hover:bg-blue-800 px-3 py-1.5 rounded-lg transition flex items-center gap-1">
              <span>${isHi ? 'पोर्टल पर आवेदन करें' : 'Apply on Portal'}</span> ↗
            </a>
          </div>
        </div>
      `;
    });
    html += `</div>`;
  } else {
    html += `<p class="text-xs text-slate-500 bg-slate-50 p-3 rounded-xl">${isHi ? 'वर्तमान फिल्टर पर कोई केंद्रीय छात्रवृत्ति नहीं मिली। कृपया राज्य छात्रवृत्ति देखें।' : 'No direct Central Scholarship matches this exact income/category filter. Please review State Scholarships below.'}</p>`;
  }
  html += `</div>`;

  // 2. State Specific Welfares & Scholarships Match
  if (data.state_info) {
    html += `
      <div class="mb-6">
        <h4 class="text-sm font-bold text-slate-900 uppercase tracking-wider mb-3 flex items-center gap-1.5">
          <i data-lucide="map-pin" class="w-4 h-4 text-emerald-600"></i>
          <span>${isHi ? `राज्य सरकार की योजनाएं (${data.state_info.state_name_hi || data.state_info.state_name})` : `State Government Schemes (${data.state_info.state_name})`}</span>
        </h4>

        <div class="bg-emerald-50/40 p-4 rounded-2xl border border-emerald-200 mb-4">
          <div class="text-xs font-bold text-emerald-950 mb-1">${isHi ? 'आधिकारिक राज्य नागरिक पोर्टल:' : 'Official State Citizen Portal:'} ${escapeHtml(data.state_info.portal_name)}</div>
          <div class="text-xs text-slate-600 mb-3">${isHi ? 'आधिकारिक स्रोत:' : 'Source:'} <a href="${data.state_info.portal_url}" target="_blank" rel="noopener noreferrer" class="text-blue-900 underline font-semibold">${data.state_info.official_source || data.state_info.portal_url}</a></div>
    `;

    // State Scholarships
    if (data.state_info.state_scholarships && data.state_info.state_scholarships.length > 0) {
      html += `<div class="font-bold text-xs text-slate-800 mb-2">${isHi ? 'राज्य छात्रवृत्ति योजनाएं:' : 'State Scholarships:'}</div><div class="space-y-2 mb-4">`;
      data.state_info.state_scholarships.forEach(ss => {
        html += `
          <div class="bg-white p-3 rounded-xl border border-emerald-200">
            <div class="font-bold text-xs text-slate-900">${escapeHtml(isHi ? (ss.name_hi || ss.name) : ss.name)}</div>
            <div class="text-xs text-slate-600 mt-0.5">${escapeHtml(ss.benefit)}</div>
            <div class="text-[11px] text-emerald-800 font-medium mt-1">आय सीमा: ${escapeHtml(ss.income_limit)}</div>
          </div>
        `;
      });
      html += `</div>`;
    }

    // State Welfares
    if (data.state_info.state_welfares && data.state_info.state_welfares.length > 0) {
      html += `<div class="font-bold text-xs text-slate-800 mb-2">${isHi ? 'राज्य सामाजिक कल्याण योजनाएं:' : 'State Welfare Programs:'}</div><div class="space-y-2">`;
      data.state_info.state_welfares.forEach(sw => {
        html += `
          <div class="bg-white p-3 rounded-xl border border-emerald-200">
            <div class="font-bold text-xs text-slate-900">${escapeHtml(isHi ? (sw.name_hi || sw.name) : sw.name)}</div>
            <div class="text-xs text-slate-600 mt-0.5">${escapeHtml(sw.description)}</div>
          </div>
        `;
      });
      html += `</div>`;
    }

    html += `
          <div class="mt-4 pt-3 border-t border-emerald-200 flex justify-end">
            <a href="${data.state_info.portal_url}" target="_blank" rel="noopener noreferrer" class="text-xs font-bold text-white bg-emerald-800 hover:bg-emerald-700 px-4 py-2 rounded-xl transition flex items-center gap-1 shadow">
              <span>${isHi ? `${data.state_info.portal_name} पोर्टल पर जाएं` : `Visit ${data.state_info.portal_name}`}</span> ↗
            </a>
          </div>
        </div>
      </div>
    `;
  }

  // 3. Certificate & Voter ID Entitlement Summary
  html += `
    <div class="mb-4">
      <h4 class="text-sm font-bold text-slate-900 uppercase tracking-wider mb-3 flex items-center gap-1.5">
        <i data-lucide="file-badge" class="w-4 h-4 text-purple-600"></i>
        <span>${isHi ? 'पात्र नागरिक प्रमाण पत्र एवं सेवाएं' : 'Eligible Certificates & Voter Services'}</span>
      </h4>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
        <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
          <div class="font-bold text-slate-900">${isHi ? 'जाति / ईडब्ल्यूएस प्रमाण पत्र' : 'Caste / EWS Certificate'}</div>
          <div class="text-slate-600 mt-0.5">${isHi ? `वर्ग: ${data.category_status.name}` : `Category: ${data.category_status.name}`}</div>
          <a href="/caste-certificate" class="text-blue-900 font-bold hover:underline block mt-2">${isHi ? 'दस्तावेज एवं नियम देखें →' : 'View Docs & Guidelines →'}</a>
        </div>
        <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
          <div class="font-bold text-slate-900">${isHi ? 'मतदाता पहचान पत्र (Voter ID)' : 'Voter ID Card (ECI)'}</div>
          <div class="text-slate-600 mt-0.5">${data.voter_status}</div>
          <a href="/voter-services" class="text-orange-900 font-bold hover:underline block mt-2">${isHi ? 'ECI फॉर्म 6 गाइड देखें →' : 'View ECI Form 6 Guide →'}</a>
        </div>
      </div>
    </div>
  `;

  container.innerHTML = html;
  lucide.createIcons();
}

// =========================================================================
// INTERACTIVE STATE DROPDOWN & POPUP MODAL HANDLER
// =========================================================================
function handleNavStateChange(stateId) {
  if (!stateId) return;
  
  // If user is on Homepage, update the homepage state hub and scroll to it
  const homeDropdown = document.getElementById('home-state-dropdown');
  if (homeDropdown) {
    homeDropdown.value = stateId;
    if (typeof loadHomeStateData === 'function') {
      loadHomeStateData();
    }
  }

  // Also pop up the full State Details Modal for instant access
  openStateDetailsModal(stateId);

  // Reset nav dropdown after selection
  const navDropdown = document.getElementById('header-state-selector');
  if (navDropdown) {
    navDropdown.value = "";
  }
}

function openStateDetailsModal(stateId) {
  const modal = document.getElementById('state-details-modal');
  const content = document.getElementById('state-modal-content');
  if (!modal || !content) return;

  const statesDb = window.ALL_STATES_DB || [];
  const st = statesDb.find(s => s.id === stateId || s.state_name.toLowerCase() === stateId.toLowerCase());
  if (!st) return;

  const isHi = (localStorage.getItem('gov_portal_lang') || 'en') === 'hi';
  const stateTitle = isHi ? (st.state_name_hi || st.state_name) : st.state_name;

  let html = `
    <div>
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6 pb-4 border-b border-slate-200">
        <div>
          <div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-bold text-emerald-800 bg-emerald-100 px-2.5 py-0.5 rounded-full border border-emerald-300">${st.type}</span>
            <span class="text-xs text-slate-500 font-medium">Government of India Citizen Services Directory</span>
          </div>
          <h2 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight font-serif">${escapeHtml(stateTitle)}</h2>
          <p class="text-xs text-slate-600 mt-1">
            ${isHi ? 'ई-गवर्नेंस एवं नागरिक सेवा पोर्टल:' : 'Official e-Governance & Citizen Portal:'} <strong>${escapeHtml(st.portal_name)}</strong>
          </p>
        </div>

        <a href="${st.portal_url}" target="_blank" rel="noopener noreferrer" class="bg-gradient-to-r from-emerald-600 to-teal-700 hover:from-emerald-700 hover:to-teal-800 text-white font-bold px-5 py-2.5 rounded-xl text-xs transition shadow-md flex items-center gap-1.5 self-start sm:self-center whitespace-nowrap">
          <span>${isHi ? 'आधिकारिक राज्य पोर्टल खोलें' : 'Open Official State Portal'}</span>
          <i data-lucide="external-link" class="w-4 h-4"></i>
        </a>
      </div>

      <!-- Verified Source Banner -->
      <div class="text-xs text-slate-700 bg-slate-50 p-3 rounded-2xl border border-slate-200 mb-6 flex items-center gap-2">
        <i data-lucide="shield-check" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
        <span><strong>${isHi ? 'सत्यापित आधिकारिक स्रोत:' : 'Verified Official Source:'}</strong> ${escapeHtml(st.official_source || st.portal_url)}</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
  `;

  // State Scholarships
  html += `
    <div>
      <h3 class="text-sm font-bold text-indigo-900 uppercase tracking-wider mb-3 flex items-center gap-2">
        <i data-lucide="graduation-cap" class="w-4 h-4 text-indigo-600"></i>
        <span>${isHi ? 'राज्य छात्रवृत्ति योजनाएं' : 'State Scholarship Schemes'}</span>
      </h3>
  `;

  if (st.state_scholarships && st.state_scholarships.length > 0) {
    html += `<div class="space-y-3">`;
    st.state_scholarships.forEach(sch => {
      html += `
        <div class="bg-indigo-50/70 p-4 rounded-2xl border border-indigo-200">
          <div class="font-bold text-sm text-indigo-950 mb-1">${escapeHtml(isHi ? (sch.name_hi || sch.name) : sch.name)}</div>
          <div class="text-xs text-slate-700 mb-2 font-medium">${escapeHtml(sch.benefit)}</div>
          <div class="text-[11px] text-indigo-900 bg-indigo-100/80 p-2 rounded-lg font-semibold mb-2">
            ${isHi ? `पात्रता: ${escapeHtml(sch.target)} | आय सीमा: ${escapeHtml(sch.income_limit)}` : `Target: ${escapeHtml(sch.target)} | Income Limit: ${escapeHtml(sch.income_limit)}`}
          </div>
          <a href="${sch.url}" target="_blank" rel="noopener noreferrer" class="text-xs font-bold text-indigo-900 hover:text-indigo-700 inline-flex items-center gap-1">
            ${isHi ? 'छात्रवृत्ति पोर्टल पर आवेदन करें' : 'Apply on Scholarship Portal'} ↗
          </a>
        </div>
      `;
    });
    html += `</div>`;
  } else {
    html += `
      <div class="bg-slate-50 p-4 rounded-2xl border border-slate-200 text-xs text-slate-600">
        ${isHi ? 'राज्य के छात्र राष्ट्रीय छात्रवृत्ति पोर्टल (NSP) के माध्यम से आवेदन कर सकते हैं।' : 'State students can apply directly through the National Scholarship Portal (NSP - scholarships.gov.in).'}
      </div>
    `;
  }
  html += `</div>`;

  // State Welfares
  html += `
    <div>
      <h3 class="text-sm font-bold text-rose-900 uppercase tracking-wider mb-3 flex items-center gap-2">
        <i data-lucide="heart-handshake" class="w-4 h-4 text-rose-600"></i>
        <span>${isHi ? 'राज्य कल्याणकारी एवं सामाजिक सुरक्षा योजनाएं' : 'State Flagship Welfare Programs'}</span>
      </h3>
  `;

  if (st.state_welfares && st.state_welfares.length > 0) {
    html += `<div class="space-y-3">`;
    st.state_welfares.forEach(w => {
      const catBadge = w.category ? `<span class="text-[10px] font-bold text-rose-800 bg-rose-100 px-2 py-0.5 rounded-full border border-rose-300 uppercase">${escapeHtml(w.category)}</span>` : '';
      const benefitHighlight = w.benefit ? `<div class="text-xs text-rose-700 font-bold mb-1 flex items-center gap-1.5"><i data-lucide="sparkles" class="w-3.5 h-3.5 text-rose-600 flex-shrink-0"></i> <span>${escapeHtml(w.benefit)}</span></div>` : '';
      html += `
        <div class="bg-rose-50/70 p-4 rounded-2xl border border-rose-200">
          <div class="flex items-center justify-between gap-2 mb-1">
            <div class="font-bold text-sm text-rose-950">${escapeHtml(isHi ? (w.name_hi || w.name) : w.name)}</div>
            ${catBadge}
          </div>
          ${benefitHighlight}
          <div class="text-xs text-slate-700 leading-relaxed">${escapeHtml(w.description)}</div>
        </div>
      `;
    });
    html += `</div>`;
  } else {
    html += `
      <div class="bg-slate-50 p-4 rounded-2xl border border-slate-200 text-xs text-slate-600">
        ${isHi ? 'राज्य e-District पोर्टल पर अन्य सामाजिक सुरक्षा एवं राजस्व योजनाएं उपलब्ध हैं।' : 'Citizen entitlements and allowances are accessible on the State e-District portal.'}
      </div>
    `;
  }
  html += `</div>`;

  html += `
      </div>
  `;

  // Key Services
  if (st.key_services && st.key_services.length > 0) {
    html += `
      <div class="pt-4 border-t border-slate-200">
        <h4 class="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
          <i data-lucide="layers" class="w-3.5 h-3.5 text-slate-600"></i>
          <span>${isHi ? 'प्रमुख ऑनलाइन नागरिक सेवाएं (e-District / Revenue)' : 'Key Online Citizen & Revenue Services'}</span>
        </h4>
        <div class="flex flex-wrap gap-2">
    `;
    st.key_services.forEach(srv => {
      html += `<span class="text-xs bg-slate-100 text-slate-800 px-3 py-1 rounded-xl border border-slate-200 font-medium">${escapeHtml(srv)}</span>`;
    });
    html += `
        </div>
      </div>
    `;
  }

  html += `
      <div class="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
        <a href="/state-directory" class="text-xs font-bold text-emerald-800 hover:underline">
          ${isHi ? 'सभी 28 राज्य एवं 8 केंद्र शासित प्रदेश देखें →' : 'View All 28 States & 8 UTs Directory →'}
        </a>
        <button onclick="closeStateDetailsModal()" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition">
          ${isHi ? 'बंद करें' : 'Close'}
        </button>
      </div>
    </div>
  `;

  content.innerHTML = html;
  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
  lucide.createIcons();
}

function closeStateDetailsModal() {
  const modal = document.getElementById('state-details-modal');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  }
}
