import { characters, gameData, uiElements, state } from './state.js';
import { startGame, triggerAction } from './game.js';

export function setupUI() {
    // Generate character selection buttons
    characters.forEach(char => {
        const btn = document.createElement('button');
        btn.className = "w-32 h-32 md:w-40 md:h-40 bg-white border-4 border-pink-400 rounded-2xl shadow-xl flex flex-col items-center justify-center gap-2 transform hover:scale-105 active:scale-95 transition-all group overflow-hidden";
        btn.onclick = () => startGame(char);
        
        btn.innerHTML = `
            <img src="characters/${char}.png" alt="${char}" class="h-20 md:h-24 object-contain group-hover:scale-110 transition-transform">
            <span class="font-bold text-pink-600 capitalize bg-pink-100 px-3 py-1 rounded-full w-full text-center text-sm md:text-base">${char}</span>
        `;
        uiElements.charSelect.appendChild(btn);
    });

    // Collect all interactables
    document.querySelectorAll('.interactable').forEach(el => {
        gameData.interactables.push({
            el: el,
            msg: el.getAttribute('data-msg'),
            action: el.getAttribute('data-action')
        });
    });

    // Keyboard bindings
    window.addEventListener('keydown', e => {
        if (e.key === 'ArrowUp' || e.key === 'w') state.keys.up = true;
        if (e.key === 'ArrowDown' || e.key === 's') state.keys.down = true;
        if (e.key === 'ArrowLeft' || e.key === 'a') state.keys.left = true;
        if (e.key === 'ArrowRight' || e.key === 'd') state.keys.right = true;
        if (e.key === ' ' || e.key === 'Enter') triggerAction();
    });

    window.addEventListener('keyup', e => {
        if (e.key === 'ArrowUp' || e.key === 'w') state.keys.up = false;
        if (e.key === 'ArrowDown' || e.key === 's') state.keys.down = false;
        if (e.key === 'ArrowLeft' || e.key === 'a') state.keys.left = false;
        if (e.key === 'ArrowRight' || e.key === 'd') state.keys.right = false;
    });

    // D-Pad Touch / Mouse
    const setupBtn = (id, key) => {
        const btn = document.getElementById(id);
        const start = (e) => { e.preventDefault(); state.keys[key] = true; };
        const end = (e) => { e.preventDefault(); state.keys[key] = false; };
        btn.addEventListener('mousedown', start);
        btn.addEventListener('touchstart', start, {passive: false});
        btn.addEventListener('mouseup', end);
        btn.addEventListener('touchend', end);
        btn.addEventListener('mouseleave', end);
    };

    setupBtn('btn-up', 'up');
    setupBtn('btn-down', 'down');
    setupBtn('btn-left', 'left');
    setupBtn('btn-right', 'right');

    // Action button
    uiElements.actionBtn.addEventListener('click', triggerAction);
    uiElements.actionBtn.addEventListener('touchstart', (e) => { e.preventDefault(); triggerAction(); }, {passive: false});

    // Lamp button
    if (uiElements.lampuBtn) {
        uiElements.lampuBtn.addEventListener('click', toggleLampu);
    }
}

export function toggleLampu() {
    gameData.isDarkMode = !gameData.isDarkMode;
    const sunMoon = document.getElementById('sun-moon');
    const sky = document.getElementById('sky');

    if (gameData.isDarkMode) {
        document.body.classList.add('dark-mode');
        sunMoon.innerText = "🌙";
        sunMoon.className = "absolute top-10 right-20 text-blue-100 text-8xl drop-shadow-[0_0_20px_rgba(219,234,254,0.8)] transition-all duration-500";
        sky.className = "absolute inset-0 bg-indigo-900 z-0 top-[60px] transition-colors duration-500";
    } else {
        document.body.classList.remove('dark-mode');
        sunMoon.innerText = "☀️";
        sunMoon.className = "absolute top-10 right-20 text-yellow-400 text-8xl drop-shadow-[0_0_20px_rgba(250,204,21,1)] transition-all duration-500";
        sky.className = "absolute inset-0 bg-blue-200 z-0 top-[60px] transition-colors duration-500";
    }
}
