document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const passwordInput = document.getElementById('password-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const generateBtn = document.getElementById('generate-btn');
    const strengthMeter = document.getElementById('strength-meter');
    const strengthLabel = document.getElementById('strength-label');
    const timeToCrack = document.getElementById('time-to-crack');
    const patternsFound = document.getElementById('patterns-found');
    const suggestions = document.getElementById('suggestions');
    const vulnerabilityDetails = document.getElementById('vulnerability-details');
    const entropyValue = document.getElementById('entropy-value');
    const lengthValue = document.getElementById('length-value');
    const charDistributionChart = document.getElementById('char-distribution');
    const securityRating = document.getElementById('security-rating');
    
    // Generate Password Form Elements
    const generateForm = document.getElementById('generate-form');
    const passwordLength = document.getElementById('password-length');
    const useUppercase = document.getElementById('use-uppercase');
    const useLowercase = document.getElementById('use-lowercase');
    const useNumbers = document.getElementById('use-numbers');
    const useSymbols = document.getElementById('use-symbols');
    const minEntropy = document.getElementById('min-entropy');
    const generatedPassword = document.getElementById('generated-password');
    
    // Language Selector
    const languageMenu = document.getElementById('language-menu');
    
    // Variables
    let chart = null;
    let currentLanguage = window.currentLanguage || 'en';
    
    // Set up language selector
    if (languageMenu) {
        // Add event listeners to language menu items
        const languageItems = languageMenu.querySelectorAll('a[data-lang]');
        languageItems.forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                const lang = this.getAttribute('data-lang');
                
                // Set language via API
                fetch('/set_language', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ language: lang })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update current language
                        currentLanguage = lang;
                        
                        // Reload the page to apply the language change
                        window.location.reload();
                    }
                })
                .catch(error => {
                    console.error('Error setting language:', error);
                });
            });
        });
    }
    
    // Confetti Configuration
    const confettiColors = ['#6e8efb', '#a777e3', '#ff6b6b', '#f7b733', '#32be8f'];
    
    // Analyze the password when clicking the button
    analyzeBtn.addEventListener('click', function() {
        const password = passwordInput.value;
        if (!password) {
            showErrorMessage('Please enter a password to analyze');
            return;
        }
        
        analyzePassword(password);
    });
    
    // Analyze the password when pressing Enter in the input
    passwordInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const password = passwordInput.value;
            if (password) {
                analyzePassword(password);
            }
        }
    });
    
    // Generate password when submitting the form
    generateForm.addEventListener('submit', function(e) {
        e.preventDefault();
        generateStrongPassword();
    });
    
    // Copy generated password to clipboard with confetti effect
    document.getElementById('copy-password').addEventListener('click', function() {
        const password = generatedPassword.textContent;
        if (password) {
            navigator.clipboard.writeText(password)
                .then(() => {
                    // Show success message
                    const copyBtn = this;
                    const originalText = copyBtn.innerHTML;
                    copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                    
                    // Trigger mini confetti
                    confetti({
                        particleCount: 30,
                        spread: 40,
                        origin: { y: 0.8 },
                        colors: confettiColors
                    });
                    
                    setTimeout(() => {
                        copyBtn.innerHTML = originalText;
                    }, 2000);
                })
                .catch(err => {
                    console.error('Failed to copy text: ', err);
                });
        }
    });
    
    // Trigger celebration for strong passwords
    function triggerCelebration() {
        const confettiCanvas = document.getElementById('confetti-container');
        
        if (!confettiCanvas) return;
        
        // First burst from the center
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 },
            colors: confettiColors
        });
        
        // Side bursts after a short delay
        setTimeout(() => {
            confetti({
                particleCount: 50,
                angle: 60,
                spread: 55,
                origin: { x: 0 },
                colors: confettiColors
            });
        }, 250);
        
        setTimeout(() => {
            confetti({
                particleCount: 50,
                angle: 120,
                spread: 55,
                origin: { x: 1 },
                colors: confettiColors
            });
        }, 400);
    }
    
    // Analyze the input password
    function analyzePassword(password) {
        // Show loading state with animation
        showLoading();
        
        // Make API request to analyze the password
        fetch('/analyze_password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                password: password,
                language: currentLanguage
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server error when analyzing password');
            }
            return response.json();
        })
        .then(data => {
            hideLoading();
            updateAnalysisResults(data);
            
            // Celebrate if it's a strong password
            if (data.score >= 80) {
                setTimeout(() => {
                    triggerCelebration();
                }, 500);
            }
        })
        .catch(error => {
            hideLoading();
            console.error('Error:', error);
            showErrorMessage('Failed to analyze password: ' + error.message);
        });
    }
    
    // Generate a strong password based on user preferences
    function generateStrongPassword() {
        // Show loading state
        document.getElementById('generate-spinner').classList.remove('d-none');
        generatedPassword.textContent = '';
        
        // Get form values
        const params = {
            length: parseInt(passwordLength.value) || 16,
            include_uppercase: useUppercase.checked,
            include_lowercase: useLowercase.checked,
            include_numbers: useNumbers.checked,
            include_symbols: useSymbols.checked,
            min_entropy: parseInt(minEntropy.value) || 80,
            language: currentLanguage
        };
        
        // Make API request to generate the password
        fetch('/generate_password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server error when generating password');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('generate-spinner').classList.add('d-none');
            
            // Display with typing animation
            const password = data.password;
            generatedPassword.textContent = '';
            
            // Type animation for the generated password
            let i = 0;
            const speed = 50; // milliseconds
            function typePassword() {
                if (i < password.length) {
                    generatedPassword.textContent += password.charAt(i);
                    i++;
                    setTimeout(typePassword, speed);
                } else {
                    // Animation complete - show confetti
                    confetti({
                        particleCount: 50,
                        spread: 70,
                        origin: { y: 0.7 },
                        colors: confettiColors
                    });
                }
            }
            
            typePassword();
            
            // Also analyze the generated password
            passwordInput.value = data.password;
            updateAnalysisResults(data.analysis);
        })
        .catch(error => {
            document.getElementById('generate-spinner').classList.add('d-none');
            console.error('Error:', error);
            showErrorMessage('Failed to generate password: ' + error.message);
        });
    }
    
    // Update the UI with analysis results
    function updateAnalysisResults(data) {
        // Update strength meter with animation
        strengthMeter.style.transition = 'width 1s cubic-bezier(0.19, 1, 0.22, 1)';
        setTimeout(() => {
            strengthMeter.style.width = data.score + '%';
            strengthMeter.setAttribute('aria-valuenow', data.score);
        }, 100);
        
        // Set the appropriate color based on score
        if (data.score < 20) {
            strengthMeter.className = 'progress-bar bg-danger';
            strengthLabel.textContent = 'Very Weak';
            strengthLabel.className = 'badge bg-danger';
        } else if (data.score < 40) {
            strengthMeter.className = 'progress-bar bg-danger';
            strengthLabel.textContent = 'Weak';
            strengthLabel.className = 'badge bg-danger';
        } else if (data.score < 60) {
            strengthMeter.className = 'progress-bar bg-warning';
            strengthLabel.textContent = 'Moderate';
            strengthLabel.className = 'badge bg-warning';
        } else if (data.score < 80) {
            strengthMeter.className = 'progress-bar bg-success';
            strengthLabel.textContent = 'Strong';
            strengthLabel.className = 'badge bg-success';
        } else {
            strengthMeter.className = 'progress-bar bg-success';
            strengthLabel.textContent = 'Very Strong';
            strengthLabel.className = 'badge bg-success';
        }
        
        // Update security rating stars
        if (securityRating) {
            const stars = securityRating.querySelectorAll('.rating-star');
            let ratingStars = 1;
            
            if (data.score >= 80) ratingStars = 5;
            else if (data.score >= 60) ratingStars = 4;
            else if (data.score >= 40) ratingStars = 3;
            else if (data.score >= 20) ratingStars = 2;
            
            stars.forEach((star, index) => {
                if (index < ratingStars) {
                    star.classList.add('active');
                } else {
                    star.classList.remove('active');
                }
            });
        }
        
        // Update detailed stats with animation
        animateCountUp(entropyValue, data.entropy);
        animateCountUp(lengthValue, data.length);
        
        // Style time to crack based on security level
        timeToCrack.textContent = data.time_to_crack;
        timeToCrack.className = 'badge rounded-pill';
        
        if (data.time_to_crack.includes('century') || data.time_to_crack.includes('million')) {
            timeToCrack.classList.add('bg-success');
        } else if (data.time_to_crack.includes('year') || data.time_to_crack.includes('month')) {
            timeToCrack.classList.add('bg-info');
        } else if (data.time_to_crack.includes('week') || data.time_to_crack.includes('day')) {
            timeToCrack.classList.add('bg-warning');
        } else {
            timeToCrack.classList.add('bg-danger');
        }
        
        // Update patterns found with animation
        patternsFound.innerHTML = '';
        
        if (data.patterns && data.patterns.length > 0) {
            data.patterns.forEach((pattern, index) => {
                setTimeout(() => {
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item';
                    listItem.innerHTML = `<i class="fas fa-exclamation-triangle me-2 text-warning"></i>${pattern}`;
                    listItem.style.opacity = '0';
                    listItem.style.transform = 'translateY(10px)';
                    listItem.style.transition = 'all 0.3s ease';
                    
                    patternsFound.appendChild(listItem);
                    
                    // Trigger animation
                    setTimeout(() => {
                        listItem.style.opacity = '1';
                        listItem.style.transform = 'translateY(0)';
                    }, 50);
                }, index * 100);
            });
        } else {
            const listItem = document.createElement('li');
            listItem.className = 'list-group-item';
            listItem.innerHTML = '<i class="fas fa-check-circle me-2 text-success"></i>No common patterns detected';
            patternsFound.appendChild(listItem);
        }
        
        // Add warning about common password
        if (data.is_common) {
            setTimeout(() => {
                const listItem = document.createElement('li');
                listItem.className = 'list-group-item';
                listItem.innerHTML = '<i class="fas fa-exclamation-circle me-2 text-danger"></i><strong>Warning:</strong> This is a commonly used password found in data breaches';
                listItem.style.opacity = '0';
                listItem.style.transition = 'opacity 0.5s ease';
                patternsFound.appendChild(listItem);
                
                // Trigger animation
                setTimeout(() => {
                    listItem.style.opacity = '1';
                }, 50);
            }, (data.patterns ? data.patterns.length : 0) * 100 + 100);
        }
        
        // Update suggestions if available
        if (data.suggestions) {
            if (typeof data.suggestions === 'string') {
                try {
                    const suggestionsObj = JSON.parse(data.suggestions);
                    updateSuggestions(suggestionsObj);
                } catch (e) {
                    console.error('Error parsing suggestions:', e);
                    suggestions.innerHTML = '<div class="alert alert-info">Could not parse suggestions.</div>';
                }
            } else {
                // Already an object (from Groq API)
                updateSuggestions(data.suggestions);
            }
        } else {
            suggestions.innerHTML = '<div class="alert alert-info">No specific suggestions available.</div>';
        }
        
        // Update character distribution chart with animation
        updateDistributionChart(data.char_distribution);
        
        // Show results section with animation
        const resultsSection = document.getElementById('results-section');
        resultsSection.classList.remove('d-none');
        resultsSection.style.opacity = '0';
        resultsSection.style.transform = 'translateY(20px)';
        resultsSection.style.transition = 'all 0.5s ease';
        
        setTimeout(() => {
            resultsSection.style.opacity = '1';
            resultsSection.style.transform = 'translateY(0)';
            // Scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        }, 100);
    }
    
    // Update the suggestions panel with enhanced UI
    function updateSuggestions(suggestionsData) {
        suggestions.innerHTML = '';
        
        // Create the main card with animation
        const card = document.createElement('div');
        card.className = 'card';
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.5s ease';
        
        // Add the award ribbon
        const ribbon = document.createElement('div');
        ribbon.className = 'ribbon';
        const ribbonSpan = document.createElement('span');
        ribbonSpan.textContent = 'AI Secured';
        ribbon.appendChild(ribbonSpan);
        card.appendChild(ribbon);
        
        const cardBody = document.createElement('div');
        cardBody.className = 'card-body';
        
        // Create improved password section with enhanced styling
        if (suggestionsData.improved_password) {
            const improvedPasswordDiv = document.createElement('div');
            improvedPasswordDiv.className = 'mb-4';
            
            const header = document.createElement('h5');
            header.className = 'mb-3';
            header.innerHTML = '<i class="fas fa-shield-alt me-2 text-success"></i>Enhanced Password:';
            improvedPasswordDiv.appendChild(header);
            
            const passwordContainer = document.createElement('div');
            passwordContainer.className = 'p-3 mb-3 rounded';
            passwordContainer.style.wordBreak = 'break-all';
            passwordContainer.style.fontFamily = 'monospace';
            passwordContainer.style.fontSize = '1.2rem';
            passwordContainer.style.fontWeight = 'bold';
            passwordContainer.style.backgroundColor = 'rgba(50, 190, 143, 0.1)';
            passwordContainer.style.border = '1px solid rgba(50, 190, 143, 0.2)';
            passwordContainer.style.color = '#38ef7d';
            passwordContainer.style.textShadow = '0 0 5px rgba(56, 239, 125, 0.3)';
            passwordContainer.style.letterSpacing = '1px';
            passwordContainer.textContent = suggestionsData.improved_password;
            improvedPasswordDiv.appendChild(passwordContainer);
            
            // Add copy button with enhanced styling
            const copyBtn = document.createElement('button');
            copyBtn.className = 'btn btn-outline-light';
            copyBtn.innerHTML = '<i class="fas fa-copy me-2"></i>Copy to Clipboard';
            copyBtn.style.transition = 'all 0.3s ease';
            
            copyBtn.addEventListener('mouseover', function() {
                this.style.boxShadow = '0 0 15px rgba(110, 142, 251, 0.4)';
            });
            
            copyBtn.addEventListener('mouseout', function() {
                this.style.boxShadow = 'none';
            });
            
            copyBtn.addEventListener('click', function() {
                navigator.clipboard.writeText(suggestionsData.improved_password)
                    .then(() => {
                        const feedback = document.createElement('span');
                        feedback.textContent = ' ✓ Copied!';
                        feedback.classList.add('text-success', 'ms-2', 'copy-feedback');
                        copyBtn.appendChild(feedback);
                        
                        // Mini confetti effect
                        confetti({
                            particleCount: 30,
                            spread: 40,
                            origin: { y: 0.8 },
                            colors: confettiColors
                        });
                        
                        setTimeout(() => {
                            feedback.remove();
                        }, 2000);
                    });
            });
            
            improvedPasswordDiv.appendChild(copyBtn);
            cardBody.appendChild(improvedPasswordDiv);
        }
        
        // Create reasoning section with enhanced styling
        if (suggestionsData.reasoning) {
            const reasoningDiv = document.createElement('div');
            reasoningDiv.className = 'mb-4';
            
            const header = document.createElement('h5');
            header.className = 'mb-3';
            header.innerHTML = '<i class="fas fa-brain me-2 text-primary"></i>Security Improvements:';
            reasoningDiv.appendChild(header);
            
            const reasoningText = document.createElement('p');
            reasoningText.className = 'p-3 rounded';
            reasoningText.style.backgroundColor = 'rgba(110, 142, 251, 0.1)';
            reasoningText.style.border = '1px solid rgba(110, 142, 251, 0.2)';
            reasoningText.textContent = suggestionsData.reasoning;
            reasoningDiv.appendChild(reasoningText);
            
            cardBody.appendChild(reasoningDiv);
        }
        
        // Create vulnerability details with animations
        if (suggestionsData.vulnerability_details && suggestionsData.vulnerability_details.length > 0) {
            const vulnerabilityDiv = document.createElement('div');
            vulnerabilityDiv.className = 'mb-3';
            
            const header = document.createElement('h5');
            header.className = 'mb-3';
            header.innerHTML = '<i class="fas fa-exclamation-triangle me-2 text-warning"></i>Vulnerability Assessment:';
            vulnerabilityDiv.appendChild(header);
            
            const vulList = document.createElement('ul');
            vulList.className = 'list-group list-group-flush';
            
            if (typeof suggestionsData.vulnerability_details === 'string') {
                const listItem = document.createElement('li');
                listItem.className = 'list-group-item';
                listItem.innerHTML = `<i class="fas fa-exclamation-circle me-2 text-warning"></i>${suggestionsData.vulnerability_details}`;
                vulList.appendChild(listItem);
            } else {
                suggestionsData.vulnerability_details.forEach((detail, index) => {
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item';
                    listItem.innerHTML = `<i class="fas fa-exclamation-circle me-2 text-warning"></i>${detail}`;
                    listItem.style.opacity = '0';
                    listItem.style.transform = 'translateY(10px)';
                    listItem.style.transition = 'all 0.3s ease';
                    listItem.style.transitionDelay = `${index * 0.1}s`;
                    vulList.appendChild(listItem);
                    
                    // Animation will be triggered after card is added to DOM
                });
            }
            
            vulnerabilityDiv.appendChild(vulList);
            cardBody.appendChild(vulnerabilityDiv);
        }
        
        card.appendChild(cardBody);
        suggestions.appendChild(card);
        
        // Trigger animations after card is in DOM
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
            
            // Animate vulnerability items
            const vulItems = card.querySelectorAll('.list-group-item');
            vulItems.forEach((item, index) => {
                setTimeout(() => {
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, 500 + index * 100);
            });
        }, 100);
    }
    
    // Animate counting up for numeric values
    function animateCountUp(element, targetValue) {
        const startValue = parseInt(element.textContent) || 0;
        const duration = 1000;
        const finalValue = parseFloat(targetValue);
        const isDecimal = String(targetValue).includes('.');
        const decimalPlaces = isDecimal ? String(targetValue).split('.')[1].length : 0;
        
        const startTime = performance.now();
        
        function updateCount(currentTime) {
            const elapsedTime = currentTime - startTime;
            const progress = Math.min(elapsedTime / duration, 1);
            // Use easeOutQuart for a nice effect
            const easeProgress = 1 - Math.pow(1 - progress, 4);
            
            const currentValue = startValue + (finalValue - startValue) * easeProgress;
            element.textContent = isDecimal ? currentValue.toFixed(decimalPlaces) : Math.floor(currentValue);
            
            if (progress < 1) {
                requestAnimationFrame(updateCount);
            }
        }
        
        requestAnimationFrame(updateCount);
    }
    
    // Update the character distribution chart with enhanced visuals
    function updateDistributionChart(distribution) {
        if (!distribution || !charDistributionChart) {
            return;
        }
        
        // Destroy existing chart if it exists
        if (chart) {
            chart.destroy();
        }
        
        // Better color palette for the chart
        const backgroundColors = [
            'rgba(110, 142, 251, 0.8)', // Primary blue
            'rgba(167, 119, 227, 0.8)', // Purple
            'rgba(255, 107, 107, 0.8)', // Red
            'rgba(50, 190, 143, 0.8)'   // Green
        ];
        
        const chartData = {
            labels: ['Lowercase', 'Uppercase', 'Digits', 'Special'],
            datasets: [{
                label: 'Character Distribution',
                data: [
                    distribution.lowercase || 0,
                    distribution.uppercase || 0,
                    distribution.digits || 0,
                    distribution.special || 0
                ],
                backgroundColor: backgroundColors,
                borderColor: backgroundColors.map(color => color.replace('0.8', '1')),
                borderWidth: 2,
                hoverOffset: 15
            }]
        };
        
        // Create new chart with enhanced options
        chart = new Chart(charDistributionChart, {
            type: 'doughnut',
            data: chartData,
            options: {
                responsive: true,
                cutout: '65%',
                animation: {
                    animateScale: true,
                    animateRotate: true,
                    duration: 1200,
                    easing: 'easeOutQuart'
                },
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#ffffff',
                            font: {
                                size: 12
                            },
                            padding: 15,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(20, 20, 20, 0.9)',
                        padding: 12,
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${percentage}% (${value} characters)`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Show loading indicator with animation
    function showLoading() {
        const spinner = document.getElementById('analyze-spinner');
        analyzeBtn.disabled = true;
        spinner.classList.remove('d-none');
    }
    
    // Hide loading indicator
    function hideLoading() {
        const spinner = document.getElementById('analyze-spinner');
        analyzeBtn.disabled = false;
        spinner.classList.add('d-none');
    }
    
    // Show error message with animation
    function showErrorMessage(message) {
        const errorDiv = document.getElementById('error-message');
        errorDiv.textContent = message;
        errorDiv.classList.remove('d-none');
        errorDiv.style.opacity = '0';
        errorDiv.style.transform = 'translateY(-10px)';
        errorDiv.style.transition = 'all 0.3s ease';
        
        // Trigger animation
        setTimeout(() => {
            errorDiv.style.opacity = '1';
            errorDiv.style.transform = 'translateY(0)';
        }, 10);
        
        // Auto hide with fade out
        setTimeout(() => {
            errorDiv.style.opacity = '0';
            errorDiv.style.transform = 'translateY(-10px)';
            
            setTimeout(() => {
                errorDiv.classList.add('d-none');
            }, 300);
        }, 5000);
    }
    
    // Initialize tooltips and popovers
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            boundary: document.body
        });
    });
    
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl, {
            html: true
        });
    });
});
