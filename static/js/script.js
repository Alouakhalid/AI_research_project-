// Global variables
let currentResearchData = null;

// DOM elements
const form = document.getElementById('researchForm');
const generateBtn = document.getElementById('generateBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsContainer = document.getElementById('resultsContainer');
const paperContent = document.getElementById('paperContent');
const paperTopic = document.getElementById('paperTopic');
const paperLanguage = document.getElementById('paperLanguage');
const paperPages = document.getElementById('paperPages');
const paperDate = document.getElementById('paperDate');
const downloadBtn = document.getElementById('downloadBtn');
const copyBtn = document.getElementById('copyBtn');
const toastContainer = document.getElementById('toastContainer');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    addFormAnimations();
});

// Event listeners
function initializeEventListeners() {
    form.addEventListener('submit', handleFormSubmit);
    downloadBtn.addEventListener('click', handleDownloadPDF);
    copyBtn.addEventListener('click', handleCopyText);
    
    // Add input animations
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('focus', addFocusAnimation);
        input.addEventListener('blur', removeFocusAnimation);
    });
}

// Form submission handler
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(form);
    const data = {
        topic: formData.get('topic'),
        language: formData.get('language'),
        pages: formData.get('pages')
    };
    
    // Validate form
    if (!data.topic.trim()) {
        showToast('Please enter a research topic', 'error');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    hideResults();
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentResearchData = result;
            displayResults(result);
            showToast('Research paper generated successfully!', 'success');
        } else {
            showToast(result.error || 'Failed to generate research paper', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Network error. Please try again.', 'error');
    } finally {
        setLoadingState(false);
    }
}

// Display results
function displayResults(data) {
    paperTopic.textContent = data.topic;
    paperLanguage.textContent = data.language;
    paperPages.textContent = data.pages + ' pages';
    paperDate.textContent = data.generated_at;
    
    // Format and display the research paper content
    const formattedContent = formatResearchPaper(data.research_paper);
    paperContent.textContent = formattedContent;
    
    // Show results with animation
    resultsContainer.style.display = 'block';
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    // Add fade-in animation
    setTimeout(() => {
        resultsContainer.style.opacity = '1';
    }, 100);
}

// Format research paper content
function formatResearchPaper(content) {
    // Clean up the content and add proper formatting
    return content
        .replace(/\*\*/g, '') // Remove bold markers
        .replace(/\*/g, '') // Remove italic markers
        .replace(/\n\n/g, '\n\n') // Preserve paragraph breaks
        .trim();
}

// Download PDF handler
async function handleDownloadPDF() {
    if (!currentResearchData) {
        showToast('No research paper to download', 'error');
        return;
    }
    
    try {
        setLoadingState(true, 'Downloading PDF...');
        
        const response = await fetch('/download_pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                research_paper: currentResearchData.research_paper,
                topic: currentResearchData.topic,
                language: currentResearchData.language
            })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${currentResearchData.topic.replace(/\s+/g, '_')}_Research_Paper.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showToast('PDF downloaded successfully!', 'success');
        } else {
            const error = await response.json();
            showToast(error.error || 'Failed to download PDF', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Network error. Please try again.', 'error');
    } finally {
        setLoadingState(false);
    }
}

// Copy text handler
function handleCopyText() {
    if (!currentResearchData) {
        showToast('No research paper to copy', 'error');
        return;
    }
    
    const textToCopy = currentResearchData.research_paper;
    
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(textToCopy).then(() => {
            showToast('Text copied to clipboard!', 'success');
        }).catch(() => {
            fallbackCopyText(textToCopy);
        });
    } else {
        fallbackCopyText(textToCopy);
    }
}

// Fallback copy method
function fallbackCopyText(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showToast('Text copied to clipboard!', 'success');
    } catch (err) {
        showToast('Failed to copy text', 'error');
    }
    
    document.body.removeChild(textArea);
}

// Loading state management
function setLoadingState(loading, text = 'Generating Research Paper...') {
    if (loading) {
        generateBtn.disabled = true;
        generateBtn.classList.add('loading');
        generateBtn.querySelector('span').textContent = text;
    } else {
        generateBtn.disabled = false;
        generateBtn.classList.remove('loading');
        generateBtn.querySelector('span').textContent = 'Generate Research Paper';
    }
}

// Hide results
function hideResults() {
    resultsContainer.style.display = 'none';
    resultsContainer.style.opacity = '0';
}

// Toast notification system
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = getToastIcon(type);
    toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    // Remove toast after 4 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 4000);
}

// Get toast icon based on type
function getToastIcon(type) {
    switch (type) {
        case 'success':
            return 'fa-check-circle';
        case 'error':
            return 'fa-exclamation-circle';
        case 'info':
        default:
            return 'fa-info-circle';
    }
}

// Form animations
function addFormAnimations() {
    const formGroups = document.querySelectorAll('.form-group');
    
    formGroups.forEach((group, index) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            group.style.transition = 'all 0.5s ease';
            group.style.opacity = '1';
            group.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Input focus animations
function addFocusAnimation(e) {
    const input = e.target;
    const label = input.previousElementSibling;
    
    if (label) {
        label.style.color = '#667eea';
        label.style.transform = 'translateY(-2px)';
    }
    
    input.style.transform = 'translateY(-2px)';
    input.style.boxShadow = '0 5px 15px rgba(102, 126, 234, 0.2)';
}

function removeFocusAnimation(e) {
    const input = e.target;
    const label = input.previousElementSibling;
    
    if (label) {
        label.style.color = '#555';
        label.style.transform = 'translateY(0)';
    }
    
    input.style.transform = 'translateY(0)';
    input.style.boxShadow = 'none';
}

// Smooth scrolling for better UX
function smoothScrollTo(element) {
    element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Add some interactive effects
document.addEventListener('mousemove', function(e) {
    const cards = document.querySelectorAll('.form-card, .results-card');
    
    cards.forEach(card => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        if (x >= 0 && x <= rect.width && y >= 0 && y <= rect.height) {
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
        } else {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
        }
    });
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (form.checkValidity()) {
            handleFormSubmit(e);
        }
    }
    
    // Escape to hide results
    if (e.key === 'Escape') {
        hideResults();
    }
});

// Add form validation feedback
const inputs = document.querySelectorAll('input[required], select[required]');
inputs.forEach(input => {
    input.addEventListener('blur', function() {
        if (!this.value.trim()) {
            this.style.borderColor = '#f44336';
            this.style.boxShadow = '0 0 0 3px rgba(244, 67, 54, 0.1)';
        } else {
            this.style.borderColor = '#4CAF50';
            this.style.boxShadow = '0 0 0 3px rgba(76, 175, 80, 0.1)';
        }
    });
    
    input.addEventListener('input', function() {
        if (this.value.trim()) {
            this.style.borderColor = '#4CAF50';
            this.style.boxShadow = '0 0 0 3px rgba(76, 175, 80, 0.1)';
        }
    });
});
