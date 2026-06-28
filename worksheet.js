
document.addEventListener('DOMContentLoaded', () => {
    // Determine level from URL or default to beginner
    const urlParams = new URLSearchParams(window.location.search);
    const level = urlParams.get('level') || 'beginner'; // 'beginner', 'intermediate', 'advanced'
    
    const quizData = worksheetData[level];
    
    if (!quizData) {
        alert("Invalid level specified!");
        return;
    }

    // UI Elements
    const startScreen = document.getElementById('startScreen');
    const quizScreen = document.getElementById('quizScreen');
    const resultScreen = document.getElementById('resultScreen');
    
    const titleEl = document.getElementById('worksheetTitle');
    const imgEl = document.getElementById('worksheetIllustration');
    
    const questionCountEl = document.getElementById('questionCount');
    const categoryBadgeEl = document.getElementById('categoryBadge');
    const progressFillEl = document.getElementById('progressFill');
    const questionTextEl = document.getElementById('questionText');
    const optionsGridEl = document.getElementById('optionsGrid');
    
    const feedbackContainer = document.getElementById('feedbackContainer');
    const feedbackIcon = document.getElementById('feedbackIcon');
    const feedbackText = document.getElementById('feedbackText');
    const explanationText = document.getElementById('explanationText');
    
    const startBtn = document.getElementById('startBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    const finalScoreEl = document.getElementById('finalScore');
    const scoreMessageEl = document.getElementById('scoreMessage');

    // Initialize UI based on level
    const levelTitles = {
        'beginner': 'Beginner Review Worksheet',
        'intermediate': 'Intermediate Review Worksheet',
        'advanced': 'Advanced Review Worksheet'
    };
    const levelImages = {
        'beginner': 'beginner_quiz.png',
        'intermediate': 'intermediate_quiz.png',
        'advanced': 'advanced_quiz.png'
    };

    titleEl.textContent = levelTitles[level];
    imgEl.src = levelImages[level];

    // Quiz State
    let currentQuestionIndex = 0;
    let score = 0;
    let vocabScore = 0;
    let grammarScore = 0;
    let vocabTotal = 0;
    let grammarTotal = 0;
    const mistakes = [];
    
    const totalQuestions = quizData.length;

    quizData.forEach(q => {
        if (q.category === 'vocab') vocabTotal++;
        else grammarTotal++;
    });

    // Shuffle questions so vocab and grammar are mixed? 
    // The user asked for "それぞれ２０問ずつのトータル４０問になるように" 
    // It's better to mix them or keep them in order? Let's keep them in order: Vocab first, then Grammar, or just shuffle them all to keep it fun!
    // Let's shuffle them to make it a real test.
    shuffleArray(quizData);

    startBtn.addEventListener('click', () => {
        startScreen.style.display = 'none';
        quizScreen.style.display = 'block';
        loadQuestion();
    });

    nextBtn.addEventListener('click', () => {
        currentQuestionIndex++;
        if (currentQuestionIndex < totalQuestions) {
            loadQuestion();
        } else {
            showResult();
        }
    });

    function loadQuestion() {
        const q = quizData[currentQuestionIndex];
        
        // Update Progress
        questionCountEl.textContent = `Question ${currentQuestionIndex + 1} / ${totalQuestions}`;
        progressFillEl.style.width = `${((currentQuestionIndex) / totalQuestions) * 100}%`;
        
        // Update Category Badge
        if (q.category === 'vocab') {
            categoryBadgeEl.textContent = 'Vocabulary';
            categoryBadgeEl.className = 'category-badge'; // red hue
        } else {
            categoryBadgeEl.textContent = 'Grammar';
            categoryBadgeEl.className = 'category-badge grammar'; // blue hue
        }

        // Set Question Text
        questionTextEl.innerHTML = q.question;
        
        // Render Options
        optionsGridEl.innerHTML = '';
        feedbackContainer.style.display = 'none';

        q.options.forEach((opt, index) => {
            const btn = document.createElement('button');
            btn.className = 'option-btn';
            btn.innerHTML = opt;
            btn.addEventListener('click', () => selectOption(index, q.answer, q.explanation, btn));
            optionsGridEl.appendChild(btn);
        });
    }

    function selectOption(selectedIndex, correctIndex, explanation, selectedBtn) {
        // Disable all buttons
        const allBtns = optionsGridEl.querySelectorAll('.option-btn');
        allBtns.forEach(btn => btn.disabled = true);

        const isCorrect = (selectedIndex === correctIndex);
        const q = quizData[currentQuestionIndex];

        if (isCorrect) {
            selectedBtn.classList.add('correct');
            score++;
            if (q.category === 'vocab') vocabScore++;
            else grammarScore++;
            showFeedback(true, explanation);
        } else {
            selectedBtn.classList.add('wrong');
            // highlight correct one
            allBtns[correctIndex].classList.add('correct');
            
            // Record mistake
            mistakes.push({
                question: q.question,
                yourAnswer: q.options[selectedIndex],
                correctAnswer: q.options[correctIndex],
                explanation: explanation
            });
            
            showFeedback(false, explanation);
        }
    }

    function showFeedback(isCorrect, explanation) {
        feedbackContainer.style.display = 'block';
        feedbackContainer.className = `feedback-container ${isCorrect ? 'correct' : 'wrong'}`;
        
        if (isCorrect) {
            feedbackIcon.textContent = '⭕️';
            feedbackText.textContent = 'Correct!';
        } else {
            feedbackIcon.textContent = '❌';
            feedbackText.textContent = 'Incorrect!';
        }
        
        explanationText.innerHTML = explanation;
    }

    function showResult() {
        quizScreen.style.display = 'none';
        resultScreen.style.display = 'block';
        
        progressFillEl.style.width = '100%';

        finalScoreEl.textContent = `${score}/${totalQuestions}`;
        
        document.getElementById('vocabScoreEl').textContent = `${vocabScore}/${vocabTotal}`;
        document.getElementById('grammarScoreEl').textContent = `${grammarScore}/${grammarTotal}`;

        const percentage = score / totalQuestions;
        if (percentage === 1) {
            scoreMessageEl.textContent = 'Perfect score! You have completely mastered this level! 🌟';
        } else if (percentage >= 0.8) {
            scoreMessageEl.textContent = 'Great job! You have a solid understanding of this level. 👏';
        } else if (percentage >= 0.6) {
            scoreMessageEl.textContent = 'Good effort! A little more review and you will be perfect. 💪';
        } else {
            scoreMessageEl.textContent = 'Keep practicing! Reviewing the lessons will help you improve. 📚';
        }
        
        if (mistakes.length > 0) {
            const mistakesContainer = document.getElementById('mistakesContainer');
            const mistakesList = document.getElementById('mistakesList');
            mistakesContainer.style.display = 'block';
            
            mistakes.forEach((m, idx) => {
                const div = document.createElement('div');
                div.style.marginBottom = '20px';
                div.style.padding = '15px';
                div.style.background = '#fff';
                div.style.borderRadius = '8px';
                div.style.borderLeft = '4px solid var(--wrong-color)';
                
                div.innerHTML = `
                    <div style="font-weight: bold; margin-bottom: 10px;">Q${idx + 1}. ${m.question}</div>
                    <div style="color: var(--wrong-color); margin-bottom: 5px;">Your Answer: ${m.yourAnswer}</div>
                    <div style="color: var(--correct-color); margin-bottom: 10px;">Correct Answer: ${m.correctAnswer}</div>
                    <div style="color: var(--secondary-color); font-size: 0.95rem;"><em>${m.explanation}</em></div>
                `;
                mistakesList.appendChild(div);
            });
        }
    }

    // Utility: Shuffle array in-place
    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }
});
