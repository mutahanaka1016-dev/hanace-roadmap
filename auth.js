import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth, onAuthStateChanged, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getFirestore, doc, getDoc, setDoc, updateDoc } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyCa6fEN_5nktmhOGESssXdEwoEjXgyl5EA",
  authDomain: "hanace-japanese.firebaseapp.com",
  databaseURL: "https://hanace-japanese-default-rtdb.firebaseio.com",
  projectId: "hanace-japanese",
  storageBucket: "hanace-japanese.firebasestorage.app",
  messagingSenderId: "1057588974120",
  appId: "1:1057588974120:web:6139687624b77c40aa5b1d",
  measurementId: "G-CNKTGS2CT0"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

window.HanaAuth = {
    user: null,
    logout() {
        signOut(auth).then(() => {
            localStorage.removeItem('hanaBananaCheatSheetProgress');
            localStorage.removeItem('hanaBananaSavedVocab');
            sessionStorage.removeItem('hanaSyncDone');
            window.location.reload();
        });
    }
};

// Intercept localStorage.setItem to also save to Firebase
const originalSetItem = localStorage.setItem;
localStorage.setItem = function(key, value) {
    originalSetItem.apply(this, arguments);
    if (window.HanaAuth.user) {
        const userRef = doc(db, "users", window.HanaAuth.user.uid);
        if (key === 'hanaBananaCheatSheetProgress') {
            try { setDoc(userRef, { cheatSheetProgress: JSON.parse(value) }, { merge: true }); } catch (e) {}
        } else if (key === 'hanaBananaSavedVocab') {
            try { setDoc(userRef, { savedVocab: JSON.parse(value) }, { merge: true }); } catch (e) {}
        }
    }
};

// Insert Auth CSS
const authStyles = `
    #hana-auth-overlay {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.8);
        backdrop-filter: blur(8px);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 999999;
        font-family: 'Quicksand', 'M PLUS Rounded 1c', sans-serif;
    }
    #hana-auth-modal {
        background: #fff;
        padding: 40px;
        border-radius: 24px;
        width: 90%;
        max-width: 400px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        text-align: center;
    }
    #hana-auth-modal h2 {
        color: #ff751f;
        margin-top: 0;
        margin-bottom: 20px;
        font-size: 1.8rem;
    }
    .hana-auth-input {
        width: 100%;
        padding: 12px 15px;
        margin-bottom: 15px;
        border: 2px solid #eee;
        border-radius: 12px;
        font-size: 1rem;
        box-sizing: border-box;
        transition: all 0.3s;
    }
    .hana-auth-input:focus {
        border-color: #ff751f;
        outline: none;
    }
    .hana-auth-btn {
        width: 100%;
        padding: 12px;
        background: #ff751f;
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        margin-bottom: 10px;
    }
    .hana-auth-btn:hover {
        background: #e66a1c;
        transform: translateY(-2px);
    }
    .hana-auth-toggle {
        background: none;
        border: none;
        color: #777;
        font-size: 0.9rem;
        cursor: pointer;
        text-decoration: underline;
    }
    .hana-auth-error {
        color: #e74c3c;
        font-size: 0.9rem;
        margin-bottom: 15px;
        display: none;
    }
    #hana-auth-loading {
        color: #fff;
        font-size: 1.5rem;
        font-weight: bold;
    }
`;

function initUI() {
    if (!document.body) {
        setTimeout(initUI, 50);
        return;
    }
    
    if (document.getElementById('hana-auth-overlay')) return;

    const styleSheet = document.createElement("style");
    styleSheet.innerText = authStyles;
    document.head.appendChild(styleSheet);

    // Create Overlay
    window.hanaAuthOverlay = document.createElement('div');
    window.hanaAuthOverlay.id = 'hana-auth-overlay';
    window.hanaAuthOverlay.innerHTML = `<div id="hana-auth-loading">Loading...</div>`;
    document.body.appendChild(window.hanaAuthOverlay);
}
initUI();

function showAuthModal() {
    let isLogin = true;
    if (!window.hanaAuthOverlay) return setTimeout(showAuthModal, 50);
    
    window.hanaAuthOverlay.innerHTML = `
        <div id="hana-auth-modal">
            <h2 id="auth-title">Log In</h2>
            <div id="auth-error" class="hana-auth-error"></div>
            <form id="auth-form">
                <input type="email" id="auth-email" class="hana-auth-input" placeholder="Email Address" required />
                <input type="password" id="auth-password" class="hana-auth-input" placeholder="Password" required />
                <button type="submit" id="auth-submit" class="hana-auth-btn">Log In</button>
            </form>
            <button id="auth-toggle" class="hana-auth-toggle">Need an account? Sign Up</button>
        </div>
    `;
    
    const form = document.getElementById('auth-form');
    const toggle = document.getElementById('auth-toggle');
    const title = document.getElementById('auth-title');
    const submitBtn = document.getElementById('auth-submit');
    const errorDiv = document.getElementById('auth-error');
    
    toggle.addEventListener('click', () => {
        isLogin = !isLogin;
        title.innerText = isLogin ? "Log In" : "Sign Up";
        submitBtn.innerText = isLogin ? "Log In" : "Sign Up";
        toggle.innerText = isLogin ? "Need an account? Sign Up" : "Already have an account? Log In";
        errorDiv.style.display = 'none';
    });
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('auth-email').value;
        const password = document.getElementById('auth-password').value;
        submitBtn.disabled = true;
        submitBtn.innerText = "Processing...";
        errorDiv.style.display = 'none';
        
        try {
            if (isLogin) {
                await signInWithEmailAndPassword(auth, email, password);
            } else {
                await createUserWithEmailAndPassword(auth, email, password);
            }
            // onAuthStateChanged will handle the rest by reloading the page once synced
        } catch (error) {
            errorDiv.innerText = error.message;
            errorDiv.style.display = 'block';
            submitBtn.disabled = false;
            submitBtn.innerText = isLogin ? "Log In" : "Sign Up";
        }
    });
}

onAuthStateChanged(auth, async (user) => {
    if (user) {
        window.HanaAuth.user = user;
        window.hanaAuthOverlay.style.display = 'none';
        
        // Add logout button to header if it exists
        const actionsDiv = document.querySelector('.header-actions');
        if (actionsDiv && !document.getElementById('logout-btn')) {
            const logoutBtn = document.createElement('button');
            logoutBtn.id = 'logout-btn';
            logoutBtn.className = 'header-action-btn';
            logoutBtn.innerText = 'Log Out';
            logoutBtn.onclick = () => window.HanaAuth.logout();
            actionsDiv.appendChild(logoutBtn);
        }
        
        // Skip sync if already done in this session
        if (sessionStorage.getItem('hanaSyncDone')) return;
        
        // Sync from Firebase
        try {
            const userRef = doc(db, "users", user.uid);
            const docSnap = await getDoc(userRef);
            let needsReload = false;
            
            if (docSnap.exists()) {
                const data = docSnap.data();
                
                // Only pull from cloud if local is empty, or if we want to force merge
                // Actually, since this is a new session, we assume Cloud is the source of truth
                // unless local has data that isn't pushed yet.
                // Safest: always accept Cloud data on a fresh session start.
                if (data.cheatSheetProgress) {
                    const cloudCheat = JSON.stringify(data.cheatSheetProgress);
                    if (cloudCheat !== localStorage.getItem('hanaBananaCheatSheetProgress')) {
                        originalSetItem.call(localStorage, 'hanaBananaCheatSheetProgress', cloudCheat);
                        needsReload = true;
                    }
                }
                
                if (data.savedVocab) {
                    const cloudVocab = JSON.stringify(data.savedVocab);
                    if (cloudVocab !== localStorage.getItem('hanaBananaSavedVocab')) {
                        originalSetItem.call(localStorage, 'hanaBananaSavedVocab', cloudVocab);
                        needsReload = true;
                    }
                }
            } else {
                // First login, push local data to Firebase
                const localCheat = localStorage.getItem('hanaBananaCheatSheetProgress');
                const localVocab = localStorage.getItem('hanaBananaSavedVocab');
                const updates = {};
                if (localCheat) updates.cheatSheetProgress = JSON.parse(localCheat);
                if (localVocab) updates.savedVocab = JSON.parse(localVocab);
                if (Object.keys(updates).length > 0) {
                    await setDoc(userRef, updates);
                }
            }
            
            sessionStorage.setItem('hanaSyncDone', 'true');
            if (needsReload) window.location.reload();
            
        } catch (e) {
            console.error("Error syncing Firebase data", e);
        }

    } else {
        window.HanaAuth.user = null;
        window.hanaAuthOverlay.style.display = 'flex';
        showAuthModal();
    }
});
