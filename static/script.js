/**
 * CivicGuide AI - Enterprise RAG Web Application Frontend Engine
 * Complete interactive controller for chat, speech, markdown, citations & theme.
 */

document.addEventListener("DOMContentLoaded", () => {
    /* ==========================================================================
       STORAGE & CONFIGURATION
       ========================================================================== */
    const STORAGE_KEY_CHATS = "civicguide_ai_chats_v2";
    const STORAGE_KEY_THEME = "civicguide_theme";
    
    const WELCOME_MESSAGE = "Hello! I am **CivicGuide AI**, your intelligent assistant for government schemes, scholarships, certificates, and civic services. How can I assist you today?";

    // State
    let chats = JSON.parse(localStorage.getItem(STORAGE_KEY_CHATS)) || [];
    let currentChatId = null;
    let isGenerating = false;
    let recognition = null;
    let isRecording = false;
    let currentUtterance = null;
    let currentlySpeakingBtn = null;

    /* ==========================================================================
       DOM ELEMENTS
       ========================================================================== */
    const chatMessages = document.getElementById("chat-messages");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const micBtn = document.getElementById("mic-btn");
    const newChatBtn = document.getElementById("new-chat-btn");
    const historyList = document.getElementById("history-list");
    const historySearch = document.getElementById("history-search");
    const clearChatBtn = document.getElementById("clear-chat-btn");
    const exportChatBtn = document.getElementById("export-chat-btn");
    const themeToggleBtn = document.getElementById("theme-toggle-btn");
    const sidebarToggleBtn = document.getElementById("sidebar-toggle-btn");
    const sidebar = document.getElementById("sidebar");
    const sidebarOverlay = document.getElementById("sidebar-overlay");
    const kbModalBtn = document.getElementById("kb-modal-btn");
    const kbModalBtnSidebar = document.getElementById("kb-modal-btn-sidebar");
    const shortcutsBtn = document.getElementById("shortcuts-btn");
    const toastContainer = document.getElementById("toast-container");

    // Modals
    const kbModal = document.getElementById("kb-modal");
    const shortcutsModal = document.getElementById("shortcuts-modal");
    const clearModal = document.getElementById("clear-modal");
    const sourceDetailModal = document.getElementById("source-detail-modal");

    /* ==========================================================================
       THEME MANAGEMENT
       ========================================================================== */
    function initTheme() {
        const savedTheme = localStorage.getItem(STORAGE_KEY_THEME);
        const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        const activeTheme = savedTheme || (systemPrefersDark ? "dark" : "light");

        document.documentElement.setAttribute("data-theme", activeTheme);
        updateThemeButton(activeTheme);
    }

    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        
        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem(STORAGE_KEY_THEME, newTheme);
        updateThemeButton(newTheme);
        showToast(`Switched to ${newTheme} theme`, "info");
    }

    function updateThemeButton(theme) {
        if (!themeToggleBtn) return;
        if (theme === "dark") {
            themeToggleBtn.innerHTML = '<i class="fa-solid fa-sun"></i><span>Light</span>';
        } else {
            themeToggleBtn.innerHTML = '<i class="fa-solid fa-moon"></i><span>Dark</span>';
        }
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", toggleTheme);
    }

    /* ==========================================================================
       TOAST NOTIFICATIONS
       ========================================================================== */
    function showToast(message, type = "info") {
        if (!toastContainer) return;

        const toast = document.createElement("div");
        toast.className = `toast toast-${type}`;
        
        let icon = "fa-circle-info";
        if (type === "success") icon = "fa-circle-check";
        if (type === "error") icon = "fa-triangle-exclamation";

        toast.innerHTML = `
            <i class="fa-solid ${icon}"></i>
            <span>${message}</span>
        `;

        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transform = "translateY(10px)";
            toast.style.transition = "all 0.3s ease";
            setTimeout(() => toast.remove(), 300);
        }, 3200);
    }

    /* ==========================================================================
       CHAT SESSIONS MANAGEMENT
       ========================================================================== */
    function saveChats() {
        localStorage.setItem(STORAGE_KEY_CHATS, JSON.stringify(chats));
    }

    function createChat() {
        const chat = {
            id: Date.now().toString(),
            title: "New Conversation",
            createdAt: new Date().toISOString(),
            messages: [
                {
                    id: "msg_" + Date.now(),
                    sender: "bot",
                    text: WELCOME_MESSAGE,
                    timestamp: formatTime(new Date()),
                    sources: []
                }
            ]
        };

        chats.unshift(chat);
        currentChatId = chat.id;
        saveChats();
        return chat;
    }

    function getCurrentChat() {
        return chats.find(chat => chat.id === currentChatId);
    }

    function formatTime(date) {
        return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function formatDateGroup(dateStr) {
        const date = new Date(dateStr);
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);

        if (date.toDateString() === today.toDateString()) {
            return "Today";
        } else if (date.toDateString() === yesterday.toDateString()) {
            return "Yesterday";
        } else {
            const diffDays = Math.floor((today - date) / (1000 * 60 * 60 * 24));
            if (diffDays <= 7) return "Previous 7 Days";
            return "Older";
        }
    }

    /* ==========================================================================
       RENDER HISTORY LIST (Grouped & Filtered)
       ========================================================================== */
    function renderHistory() {
        if (!historyList) return;
        historyList.innerHTML = "";

        const searchQuery = historySearch ? historySearch.value.toLowerCase().trim() : "";
        const filteredChats = chats.filter(chat => 
            chat.title.toLowerCase().includes(searchQuery)
        );

        if (filteredChats.length === 0) {
            historyList.innerHTML = `
                <div class="history-empty-state">
                    <i class="fa-regular fa-comments" style="font-size: 24px; margin-bottom: 8px; display:block;"></i>
                    ${searchQuery ? "No matching conversations" : "No conversations yet"}
                </div>
            `;
            return;
        }

        // Group chats
        const groups = {};
        filteredChats.forEach(chat => {
            const groupName = formatDateGroup(chat.createdAt || new Date());
            if (!groups[groupName]) groups[groupName] = [];
            groups[groupName].push(chat);
        });

        const groupOrder = ["Today", "Yesterday", "Previous 7 Days", "Older"];

        groupOrder.forEach(groupName => {
            if (groups[groupName] && groups[groupName].length > 0) {
                const groupTitle = document.createElement("div");
                groupTitle.className = "history-group-title";
                groupTitle.textContent = groupName;
                historyList.appendChild(groupTitle);

                const groupList = document.createElement("div");
                groupList.className = "history-list";

                groups[groupName].forEach(chat => {
                    const item = document.createElement("li");
                    item.className = `history-item ${chat.id === currentChatId ? "active" : ""}`;
                    item.dataset.id = chat.id;

                    item.innerHTML = `
                        <div class="history-item-content">
                            <i class="fa-regular fa-message history-item-icon"></i>
                            <span class="history-item-title" title="${escapeHtml(chat.title)}">${escapeHtml(chat.title)}</span>
                        </div>
                        <div class="history-item-actions">
                            <button class="history-action-btn rename-btn" title="Rename"><i class="fa-solid fa-pen"></i></button>
                            <button class="history-action-btn delete-btn" title="Delete"><i class="fa-solid fa-trash-can"></i></button>
                        </div>
                    `;

                    groupList.appendChild(item);
                });

                historyList.appendChild(groupList);
            }
        });
    }

    if (historySearch) {
        historySearch.addEventListener("input", renderHistory);
    }

    /* ==========================================================================
       HISTORY ACTIONS (Click, Rename, Delete)
       ========================================================================== */
    if (historyList) {
        historyList.addEventListener("click", (e) => {
            const historyItem = e.target.closest(".history-item");
            if (!historyItem) return;

            const chatId = historyItem.dataset.id;

            // Delete
            const deleteBtn = e.target.closest(".delete-btn");
            if (deleteBtn) {
                e.stopPropagation();
                deleteChat(chatId);
                return;
            }

            // Rename
            const renameBtn = e.target.closest(".rename-btn");
            if (renameBtn) {
                e.stopPropagation();
                renameChat(chatId);
                return;
            }

            // Switch Chat
            currentChatId = chatId;
            renderHistory();
            renderCurrentChat();

            // Mobile close sidebar
            if (window.innerWidth <= 768) {
                closeMobileSidebar();
            }
        });
    }

    function deleteChat(chatId) {
        chats = chats.filter(c => c.id !== chatId);
        if (currentChatId === chatId) {
            if (chats.length > 0) {
                currentChatId = chats[0].id;
            } else {
                createChat();
            }
        }
        saveChats();
        renderHistory();
        renderCurrentChat();
        showToast("Conversation deleted", "info");
    }

    function renameChat(chatId) {
        const chat = chats.find(c => c.id === chatId);
        if (!chat) return;

        const newTitle = prompt("Enter new title for this conversation:", chat.title);
        if (newTitle && newTitle.trim()) {
            chat.title = newTitle.trim();
            saveChats();
            renderHistory();
            showToast("Conversation renamed", "success");
        }
    }

    /* ==========================================================================
       HERO PROMPT CARDS & EMPTY STATE
       ========================================================================== */
    function renderHero() {
        return `
            <div class="welcome-hero">
                <div class="hero-emblem">
                    <i class="fa-solid fa-graduation-cap"></i>
                </div>
                <h2 class="hero-title">Indian Exams & Civic Services Knowledge Guide</h2>
                <p class="hero-subtitle">
                    Comprehensive AI guidance on major national entrance exams, civil services, defence & military careers, railways, state police, and government welfare schemes.
                </p>
                <div class="prompt-cards-grid">
                    <div class="prompt-card" data-prompt="What is the eligibility, age limit, attempts, and 3-stage exam pattern for UPSC Civil Services (IAS/IPS/IFS)?">
                        <div class="prompt-card-header">
                            <span class="prompt-card-badge">UPSC CSE</span>
                            <i class="fa-solid fa-landmark prompt-card-icon"></i>
                        </div>
                        <div class="prompt-card-title">UPSC Civil Services (IAS/IPS)</div>
                        <div class="prompt-card-desc">Prelims GS & CSAT, Mains 9 papers, optional subjects, and interview process.</div>
                    </div>

                    <div class="prompt-card" data-prompt="How can I join the Indian Armed Forces through NDA, CDS, AFCAT, or the Agniveer Scheme? What are the physical and written exam stages?">
                        <div class="prompt-card-header">
                            <span class="prompt-card-badge">Defence</span>
                            <i class="fa-solid fa-shield-halved prompt-card-icon"></i>
                        </div>
                        <div class="prompt-card-title">Defence & Military Careers</div>
                        <div class="prompt-card-desc">NDA after 12th, CDS/AFCAT for graduates, 5-day SSB interview, and Agniveer.</div>
                    </div>

                    <div class="prompt-card" data-prompt="Explain the selection process, eligibility, syllabus, and physical tests for RRB NTPC, Group D, and Assistant Loco Pilot (ALP).">
                        <div class="prompt-card-header">
                            <span class="prompt-card-badge">Railways</span>
                            <i class="fa-solid fa-train prompt-card-icon"></i>
                        </div>
                        <div class="prompt-card-title">Railway Recruitments (RRB)</div>
                        <div class="prompt-card-desc">CBT-1, CBT-2, trade tests, CBAT aptitude, and Group D physical efficiency tests.</div>
                    </div>

                    <div class="prompt-card" data-prompt="What are the physical test standards (PET/PST), age limits, and written exam syllabus for State Police Sub-Inspector (SI) and State PSC exams?">
                        <div class="prompt-card-header">
                            <span class="prompt-card-badge">Police & PSC</span>
                            <i class="fa-solid fa-user-shield prompt-card-icon"></i>
                        </div>
                        <div class="prompt-card-title">State Police SI & State PSCs</div>
                        <div class="prompt-card-desc">Running, height/chest standards, language paper, and state civil services (KAS/PCS).</div>
                    </div>

                    <div class="prompt-card" data-prompt="What is the difference in eligibility, syllabus, and exam pattern between JEE Main, JEE Advanced, and NEET UG?">
                        <div class="prompt-card-header">
                            <span class="prompt-card-badge">Entrances</span>
                            <i class="fa-solid fa-flask-vial prompt-card-icon"></i>
                        </div>
                        <div class="prompt-card-title">JEE (IIT) & NEET (Medical)</div>
                        <div class="prompt-card-desc">Class 12 criteria (75% rule), PCM/PCB subjects, scoring pattern, and NTA portals.</div>
                    </div>

                    <div class="prompt-card" data-prompt="What are the eligibility criteria, documents required, and application steps for the PM-USP scholarship and Income/Caste certificates?">
                        <div class="prompt-card-header">
                            <span class="prompt-card-badge">Welfare</span>
                            <i class="fa-solid fa-award prompt-card-icon"></i>
                        </div>
                        <div class="prompt-card-title">Govt Scholarships & Certificates</div>
                        <div class="prompt-card-desc">NSP portal, PM-USP financial benefits, and certificate verification channels.</div>
                    </div>
                </div>
            </div>
        `;
    }

    // Attach click listeners to prompt cards
    chatMessages.addEventListener("click", (e) => {
        const card = e.target.closest(".prompt-card");
        if (card && card.dataset.prompt) {
            userInput.value = card.dataset.prompt;
            handleSend();
        }
    });

    /* ==========================================================================
       MARKDOWN RENDERING & CODE HIGHLIGHTING
       ========================================================================== */
    function renderMarkdown(rawText) {
        if (typeof marked !== "undefined" && typeof DOMPurify !== "undefined") {
            marked.setOptions({
                gfm: true,
                breaks: true,
                smartypants: true
            });
            const html = marked.parse(rawText || "");
            return DOMPurify.sanitize(html);
        }
        return escapeHtml(rawText);
    }

    function escapeHtml(str) {
        if (!str) return "";
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    /* ==========================================================================
       RENDER CURRENT CHAT
       ========================================================================== */
    function renderCurrentChat() {
        chatMessages.innerHTML = "";
        const currentChat = getCurrentChat();
        if (!currentChat) return;

        // If only welcome message exists, show hero screen
        if (currentChat.messages.length === 1 && currentChat.messages[0].sender === "bot") {
            chatMessages.innerHTML = renderHero();
            return;
        }

        currentChat.messages.forEach(msg => {
            renderMessageNode(msg);
        });

        if (window.hljs) {
            hljs.highlightAll();
        }

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    /* ==========================================================================
       RENDER MESSAGE NODE
       ========================================================================== */
    function renderMessageNode(msg) {
        const row = document.createElement("div");
        row.className = `message-row ${msg.sender}-row`;

        if (msg.sender === "user") {
            row.innerHTML = `
                <div class="user-message-container">
                    <div class="message-bubble user">${escapeHtml(msg.text)}</div>
                    <div class="message-meta">${msg.timestamp || formatTime(new Date())}</div>
                </div>
            `;
        } else {
            const hasSources = msg.sources && msg.sources.length > 0;
            let sourcesHtml = "";

            if (hasSources) {
                const badges = msg.sources.map(src => {
                    const confidenceText = src.confidence ? `• ${src.confidence}% Match` : '';
                    return `
                        <button class="source-badge" data-source="${escapeHtml(src.source)}" data-chunk="${src.chunk_number}" data-confidence="${src.confidence || 0}">
                            <i class="fa-solid fa-file-lines"></i>
                            <span>${escapeHtml(src.source)} (Chunk ${src.chunk_number})</span>
                            <strong style="color: var(--primary);">${confidenceText}</strong>
                        </button>
                    `;
                }).join("");

                sourcesHtml = `
                    <div class="sources-section">
                        <div class="sources-header">
                            <div class="sources-header-title">
                                <i class="fa-solid fa-book-bookmark" style="color: var(--primary);"></i>
                                <span>Verified Knowledge Sources (${msg.sources.length})</span>
                            </div>
                            <i class="fa-solid fa-chevron-down" style="font-size: 11px;"></i>
                        </div>
                        <div class="sources-badges-container">
                            ${badges}
                        </div>
                    </div>
                `;
            }

            const confidenceBadge = msg.confidence ? `
                <span class="rag-confidence-badge" title="RAG Retrieval Confidence">
                    <i class="fa-solid fa-bullseye"></i> ${msg.confidence}% Relevance
                </span>
            ` : '';

            row.innerHTML = `
                <div class="bot-message-container" data-msg-id="${msg.id || ''}">
                    <div class="bot-header">
                        <div class="bot-profile">
                            <div class="bot-avatar">
                                <i class="fa-solid fa-robot"></i>
                            </div>
                            <div>
                                <div class="bot-name">CivicGuide AI</div>
                            </div>
                        </div>
                        <div class="bot-meta-tags">
                            ${confidenceBadge}
                            <span class="message-meta">${msg.timestamp || formatTime(new Date())}</span>
                        </div>
                    </div>
                    <div class="bot-content">${renderMarkdown(msg.text)}</div>
                    ${sourcesHtml}
                    <div class="bot-actions-toolbar">
                        <div class="actions-left">
                            <button class="btn-msg-action btn-copy-msg" title="Copy response to clipboard">
                                <i class="fa-regular fa-copy"></i>
                                <span>Copy</span>
                            </button>
                            <button class="btn-msg-action btn-speak-msg" title="Read answer aloud">
                                <i class="fa-solid fa-volume-high"></i>
                                <span>Listen</span>
                            </button>
                            <button class="btn-msg-action btn-regen-msg" title="Regenerate response">
                                <i class="fa-solid fa-arrows-rotate"></i>
                                <span>Regenerate</span>
                            </button>
                        </div>
                        <div class="actions-right">
                            <button class="btn-msg-action btn-like-msg" title="Good answer">
                                <i class="fa-regular fa-thumbs-up"></i>
                            </button>
                            <button class="btn-msg-action btn-dislike-msg" title="Poor answer">
                                <i class="fa-regular fa-thumbs-down"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }

        chatMessages.appendChild(row);
    }

    /* ==========================================================================
       MESSAGE ACTIONS (Copy, Speech, Feedback, Sources)
       ========================================================================== */
    chatMessages.addEventListener("click", async (e) => {
        // Copy message
        const copyBtn = e.target.closest(".btn-copy-msg");
        if (copyBtn) {
            const botContainer = copyBtn.closest(".bot-message-container");
            const content = botContainer.querySelector(".bot-content").innerText;
            navigator.clipboard.writeText(content).then(() => {
                copyBtn.innerHTML = '<i class="fa-solid fa-check" style="color: var(--accent-emerald);"></i><span>Copied!</span>';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fa-regular fa-copy"></i><span>Copy</span>';
                }, 2000);
            });
            return;
        }

        // Text to Speech
        const speakBtn = e.target.closest(".btn-speak-msg");
        if (speakBtn) {
            handleSpeak(speakBtn);
            return;
        }

        // Feedback: Like / Dislike
        const likeBtn = e.target.closest(".btn-like-msg");
        if (likeBtn) {
            likeBtn.classList.toggle("active-like");
            const dislikeBtn = likeBtn.parentElement.querySelector(".btn-dislike-msg");
            dislikeBtn.classList.remove("active-dislike");
            sendFeedback("like");
            return;
        }

        const dislikeBtn = e.target.closest(".btn-dislike-msg");
        if (dislikeBtn) {
            dislikeBtn.classList.toggle("active-dislike");
            const likeBtn = dislikeBtn.parentElement.querySelector(".btn-like-msg");
            likeBtn.classList.remove("active-like");
            sendFeedback("dislike");
            return;
        }

        // Regenerate
        const regenBtn = e.target.closest(".btn-regen-msg");
        if (regenBtn) {
            const currentChat = getCurrentChat();
            if (currentChat && currentChat.messages.length >= 2) {
                // Find last user query
                const userMsgs = currentChat.messages.filter(m => m.sender === "user");
                if (userMsgs.length > 0) {
                    const lastQuery = userMsgs[userMsgs.length - 1].text;
                    userInput.value = lastQuery;
                    handleSend();
                }
            }
            return;
        }

        // Source badge click -> Open Source Detail Modal
        const sourceBadge = e.target.closest(".source-badge");
        if (sourceBadge) {
            const sourceName = sourceBadge.dataset.source;
            const chunkNum = sourceBadge.dataset.chunk;
            const confidence = sourceBadge.dataset.confidence;
            openSourceModal(sourceName, chunkNum, confidence);
            return;
        }
    });

    /* ==========================================================================
       TEXT-TO-SPEECH (TTS)
       ========================================================================== */
    function handleSpeak(btn) {
        if (!("speechSynthesis" in window)) {
            showToast("Text-to-Speech is not supported in your browser.", "error");
            return;
        }

        if (window.speechSynthesis.speaking) {
            window.speechSynthesis.cancel();
            if (currentlySpeakingBtn) {
                currentlySpeakingBtn.innerHTML = '<i class="fa-solid fa-volume-high"></i><span>Listen</span>';
                currentlySpeakingBtn.classList.remove("speaking");
            }
            if (currentlySpeakingBtn === btn) {
                currentlySpeakingBtn = null;
                return;
            }
        }

        const botContainer = btn.closest(".bot-message-container");
        const content = botContainer.querySelector(".bot-content").innerText;

        currentUtterance = new SpeechSynthesisUtterance(content);
        currentUtterance.rate = 1.0;
        currentUtterance.pitch = 1.0;

        btn.innerHTML = '<i class="fa-solid fa-circle-stop"></i><span>Stop</span>';
        btn.classList.add("speaking");
        currentlySpeakingBtn = btn;

        currentUtterance.onend = () => {
            btn.innerHTML = '<i class="fa-solid fa-volume-high"></i><span>Listen</span>';
            btn.classList.remove("speaking");
            currentlySpeakingBtn = null;
        };

        currentUtterance.onerror = () => {
            btn.innerHTML = '<i class="fa-solid fa-volume-high"></i><span>Listen</span>';
            btn.classList.remove("speaking");
            currentlySpeakingBtn = null;
        };

        window.speechSynthesis.speak(currentUtterance);
    }

    /* ==========================================================================
       SPEECH-TO-TEXT (Voice Recognition)
       ========================================================================== */
    function initSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            if (micBtn) {
                micBtn.title = "Voice recognition not supported";
                micBtn.style.opacity = "0.4";
            }
            return;
        }

        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";

        recognition.onstart = () => {
            isRecording = true;
            micBtn.classList.add("recording");
            showToast("Listening... Speak your question", "info");
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            autoResizeTextarea();
            userInput.focus();
        };

        recognition.onerror = (event) => {
            console.error("Speech recognition error:", event.error);
            showToast("Voice recognition error: " + event.error, "error");
            stopRecording();
        };

        recognition.onend = () => {
            stopRecording();
        };
    }

    function toggleRecording() {
        if (!recognition) {
            showToast("Voice recognition not supported in this browser.", "error");
            return;
        }

        if (isRecording) {
            recognition.stop();
            stopRecording();
        } else {
            recognition.start();
        }
    }

    function stopRecording() {
        isRecording = false;
        if (micBtn) micBtn.classList.remove("recording");
    }

    if (micBtn) {
        initSpeechRecognition();
        micBtn.addEventListener("click", toggleRecording);
    }

    /* ==========================================================================
       SEND QUESTION & STREAM/LOADING STATE
       ========================================================================== */
    async function handleSend() {
        const question = userInput.value.trim();
        if (!question || isGenerating) return;

        const currentChat = getCurrentChat();
        if (!currentChat) return;

        // Auto-update conversation title from first question
        if (currentChat.title === "New Conversation") {
            currentChat.title = question.length > 32 ? question.substring(0, 32) + "..." : question;
            renderHistory();
        }

        // Add user message to session
        const userMsg = {
            id: "msg_" + Date.now(),
            sender: "user",
            text: question,
            timestamp: formatTime(new Date())
        };

        currentChat.messages.push(userMsg);
        saveChats();

        // Clear input and resize
        userInput.value = "";
        autoResizeTextarea();

        // Re-render feed
        renderCurrentChat();

        // Show Skeleton Loading
        showLoadingSkeleton();
        isGenerating = true;
        sendBtn.disabled = true;

        try {
            const response = await fetch("/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: question })
            });

            const data = await response.json();
            removeLoadingSkeleton();

            if (!response.ok) {
                const errorMsg = {
                    id: "msg_" + Date.now(),
                    sender: "bot",
                    text: data.detail || "Error communicating with CivicGuide backend.",
                    timestamp: formatTime(new Date()),
                    sources: []
                };
                currentChat.messages.push(errorMsg);
            } else {
                const botMsg = {
                    id: "msg_" + Date.now(),
                    sender: "bot",
                    text: data.answer || "I could not find this information in the available documents.",
                    timestamp: formatTime(new Date()),
                    sources: data.sources || [],
                    confidence: data.confidence || 0
                };
                currentChat.messages.push(botMsg);
            }

            saveChats();
            renderCurrentChat();

        } catch (error) {
            console.error("API error:", error);
            removeLoadingSkeleton();

            const networkErrorMsg = {
                id: "msg_" + Date.now(),
                sender: "bot",
                text: "⚠️ **Connection Error**: Unable to reach the CivicGuide backend server. Please make sure the FastAPI server is running.",
                timestamp: formatTime(new Date()),
                sources: []
            };
            currentChat.messages.push(networkErrorMsg);
            saveChats();
            renderCurrentChat();
        } finally {
            isGenerating = false;
            sendBtn.disabled = false;
            userInput.focus();
        }
    }

    function showLoadingSkeleton() {
        const row = document.createElement("div");
        row.className = "message-row bot-row";
        row.id = "loading-row";

        row.innerHTML = `
            <div class="loading-container">
                <div class="loading-header">
                    <div class="bot-avatar" style="width: 28px; height: 28px; font-size: 12px;">
                        <i class="fa-solid fa-brain"></i>
                    </div>
                    <span class="loading-step-text">Searching knowledge base & synthesizing answer...</span>
                </div>
                <div class="shimmer-line full"></div>
                <div class="shimmer-line long"></div>
                <div class="shimmer-line medium"></div>
            </div>
        `;

        chatMessages.appendChild(row);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeLoadingSkeleton() {
        const loadingRow = document.getElementById("loading-row");
        if (loadingRow) loadingRow.remove();
    }

    /* ==========================================================================
       TEXTAREA AUTO-RESIZE & KEYBOARD LISTENERS
       ========================================================================== */
    function autoResizeTextarea() {
        userInput.style.height = "auto";
        userInput.style.height = Math.min(userInput.scrollHeight, 160) + "px";
    }

    userInput.addEventListener("input", autoResizeTextarea);

    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });

    sendBtn.addEventListener("click", handleSend);

    /* Quick Topic Chips click */
    document.querySelectorAll(".chip-btn").forEach(chip => {
        chip.addEventListener("click", () => {
            const query = chip.dataset.query;
            if (query) {
                userInput.value = query;
                autoResizeTextarea();
                handleSend();
            }
        });
    });

    /* ==========================================================================
       EXPORT CONVERSATION (Markdown / Plain Text)
       ========================================================================== */
    if (exportChatBtn) {
        exportChatBtn.addEventListener("click", () => {
            const currentChat = getCurrentChat();
            if (!currentChat || currentChat.messages.length === 0) {
                showToast("No messages to export.", "info");
                return;
            }

            let mdContent = `# ${currentChat.title}\n*Exported from CivicGuide AI on ${new Date().toLocaleString()}*\n\n---\n\n`;
            currentChat.messages.forEach(msg => {
                const role = msg.sender === "user" ? "### 👤 User" : "### 🏛️ CivicGuide AI";
                mdContent += `${role} *(${msg.timestamp})*\n\n${msg.text}\n\n`;
                if (msg.sources && msg.sources.length > 0) {
                    mdContent += `**Sources:** ${msg.sources.map(s => `${s.source} (Chunk ${s.chunk_number})`).join(", ")}\n\n`;
                }
                mdContent += `---\n\n`;
            });

            const blob = new Blob([mdContent], { type: "text/markdown;charset=utf-8" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `${currentChat.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}_export.md`;
            a.click();
            URL.revokeObjectURL(url);
            showToast("Conversation exported as Markdown", "success");
        });
    }

    /* ==========================================================================
       CLEAR CONVERSATION MODAL
       ========================================================================== */
    if (clearChatBtn) {
        clearChatBtn.addEventListener("click", () => {
            openModal(clearModal);
        });
    }

    const confirmClearBtn = document.getElementById("confirm-clear-btn");
    if (confirmClearBtn) {
        confirmClearBtn.addEventListener("click", () => {
            const currentChat = getCurrentChat();
            if (currentChat) {
                currentChat.messages = [
                    {
                        id: "msg_" + Date.now(),
                        sender: "bot",
                        text: WELCOME_MESSAGE,
                        timestamp: formatTime(new Date()),
                        sources: []
                    }
                ];
                currentChat.title = "New Conversation";
                saveChats();
                renderCurrentChat();
                renderHistory();
                closeModal(clearModal);
                showToast("Conversation cleared", "info");
            }
        });
    }

    /* ==========================================================================
       NEW CHAT BUTTON
       ========================================================================== */
    if (newChatBtn) {
        newChatBtn.addEventListener("click", () => {
            createChat();
            renderHistory();
            renderCurrentChat();
            userInput.focus();
            if (window.innerWidth <= 768) closeMobileSidebar();
        });
    }

    /* ==========================================================================
       KNOWLEDGE BASE EXPLORER MODAL
       ========================================================================== */
    async function loadKnowledgeBaseStats() {
        const statsGrid = document.getElementById("kb-stats-grid");
        const docList = document.getElementById("kb-doc-list");

        try {
            const response = await fetch("/api/documents");
            const data = await response.json();

            if (statsGrid) {
                statsGrid.innerHTML = `
                    <div class="modal-stat-box">
                        <div class="stat-number">${data.total_documents}</div>
                        <div class="stat-label">Total Documents</div>
                    </div>
                    <div class="modal-stat-box">
                        <div class="stat-number">${data.total_chunks}</div>
                        <div class="stat-label">Indexed Chunks</div>
                    </div>
                    <div class="modal-stat-box">
                        <div class="stat-number" style="font-size: 15px; font-weight: 600;">${data.embedding_model}</div>
                        <div class="stat-label">Embedding Model</div>
                    </div>
                    <div class="modal-stat-box">
                        <div class="stat-number" style="font-size: 15px; font-weight: 600;">${data.llm_model}</div>
                        <div class="stat-label">LLM Service</div>
                    </div>
                `;
            }

            if (docList && data.documents) {
                docList.innerHTML = data.documents.map(doc => `
                    <li class="kb-doc-item">
                        <div class="kb-doc-info">
                            <i class="fa-solid ${doc.extension === 'pdf' ? 'fa-file-pdf' : 'fa-file-lines'}" style="color: ${doc.extension === 'pdf' ? 'var(--accent-rose)' : 'var(--primary)'}; font-size: 18px;"></i>
                            <div>
                                <strong style="color: var(--text-primary); font-size: 13px;">${escapeHtml(doc.name)}</strong>
                                <div style="font-size: 11px; color: var(--text-muted);">${doc.size_kb} KB · ${doc.chunks} Chunks</div>
                            </div>
                        </div>
                        <span class="kb-doc-badge">${doc.extension.toUpperCase()}</span>
                    </li>
                `).join("");
            }
        } catch (error) {
            console.error("Failed to load KB stats:", error);
        }
    }

    if (kbModalBtn) {
        kbModalBtn.addEventListener("click", () => {
            loadKnowledgeBaseStats();
            openModal(kbModal);
        });
    }

    if (kbModalBtnSidebar) {
        kbModalBtnSidebar.addEventListener("click", () => {
            loadKnowledgeBaseStats();
            openModal(kbModal);
        });
    }

    /* Source Detail Modal */
    function openSourceModal(sourceName, chunkNumber, confidence) {
        const titleEl = document.getElementById("source-modal-title");
        const bodyEl = document.getElementById("source-modal-body");
        if (titleEl) titleEl.textContent = `${sourceName} (Chunk #${chunkNumber})`;
        if (bodyEl) {
            bodyEl.innerHTML = `
                <div style="background: var(--bg-surface-elevated); padding: 14px; border-radius: 8px; border: 1px solid var(--border-subtle); margin-bottom: 12px;">
                    <div style="display: flex; gap: 16px; font-size: 12px; color: var(--text-secondary);">
                        <div><strong>Document:</strong> ${escapeHtml(sourceName)}</div>
                        <div><strong>Chunk Index:</strong> #${chunkNumber}</div>
                        <div><strong>Relevance Score:</strong> ${confidence}%</div>
                    </div>
                </div>
                <p style="font-size: 13px; color: var(--text-muted);">
                    This chunk from <code>${escapeHtml(sourceName)}</code> was retrieved via vector similarity search using MiniLM embeddings and verified by Cohere Command-R to answer your inquiry.
                </p>
            `;
        }
        openModal(sourceDetailModal);
    }

    /* ==========================================================================
       MODAL CONTROLLERS & SHORTCUTS
       ========================================================================== */
    function openModal(modal) {
        if (!modal) return;
        modal.classList.add("active");
    }

    function closeModal(modal) {
        if (!modal) return;
        modal.classList.remove("active");
    }

    document.querySelectorAll(".btn-modal-close, .modal-backdrop").forEach(el => {
        el.addEventListener("click", (e) => {
            if (e.target === el || el.classList.contains("btn-modal-close")) {
                const activeModal = el.closest(".modal-backdrop") || el;
                closeModal(activeModal);
            }
        });
    });

    if (shortcutsBtn) {
        shortcutsBtn.addEventListener("click", () => {
            openModal(shortcutsModal);
        });
    }

    // Keyboard Shortcuts
    document.addEventListener("keydown", (e) => {
        // Ctrl+N -> New Chat
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "n") {
            e.preventDefault();
            createChat();
            renderHistory();
            renderCurrentChat();
            userInput.focus();
        }
        // Ctrl+K -> Search History
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
            e.preventDefault();
            if (historySearch) historySearch.focus();
        }
        // Ctrl+Shift+D -> Toggle Theme
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === "d") {
            e.preventDefault();
            toggleTheme();
        }
        // Esc -> Close Modals
        if (e.key === "Escape") {
            document.querySelectorAll(".modal-backdrop.active").forEach(closeModal);
        }
        // ? -> Shortcuts Modal (if not typing in input)
        if (e.key === "?" && document.activeElement !== userInput && document.activeElement !== historySearch) {
            e.preventDefault();
            openModal(shortcutsModal);
        }
    });

    /* ==========================================================================
       SIDEBAR TOGGLE & MOBILE DRAWER
       ========================================================================== */
    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener("click", () => {
            if (window.innerWidth <= 768) {
                sidebar.classList.toggle("mobile-open");
                sidebarOverlay.classList.toggle("active");
            } else {
                sidebar.classList.toggle("collapsed");
            }
        });
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener("click", closeMobileSidebar);
    }

    function closeMobileSidebar() {
        if (sidebar) sidebar.classList.remove("mobile-open");
        if (sidebarOverlay) sidebarOverlay.classList.remove("active");
    }

    /* Feedback endpoint */
    async function sendFeedback(rating) {
        showToast(rating === "like" ? "Thank you for the positive feedback!" : "Feedback recorded.", "success");
        try {
            await fetch("/api/feedback", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: "UI Interaction", rating: rating })
            });
        } catch (e) {
            console.warn("Feedback endpoint error:", e);
        }
    }

    /* ==========================================================================
       INITIALIZE APP
       ========================================================================== */
    initTheme();

    if (chats.length === 0) {
        const newChat = createChat();
        currentChatId = newChat.id;
    } else {
        currentChatId = chats[0].id;
    }

    renderHistory();
    renderCurrentChat();
});