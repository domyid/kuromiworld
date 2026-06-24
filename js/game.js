import { characters, gameData, uiElements, state } from './state.js';

export function startGame(selectedChar) {
    uiElements.startScreen.style.display = 'none';

    // Buat Player
    gameData.player = document.createElement('div');
    gameData.player.className = 'entity player';
    gameData.player.style.backgroundImage = `url('characters/${selectedChar}.png')`;
    
    // Balon Chat Player
    const chatBubble = document.createElement('div');
    chatBubble.className = 'chat-bubble';
    chatBubble.id = 'player-chat';
    gameData.player.appendChild(chatBubble);
    
    uiElements.entities.appendChild(gameData.player);

    // Buat NPC dari sisa karakter
    let npcXPos = 500;
    characters.forEach(char => {
        if (char === selectedChar) return;
        
        const npc = document.createElement('div');
        npc.className = 'entity';
        npc.style.backgroundImage = `url('characters/${char}.png')`;
        
        // Tambahkan sedikit variasi ukuran/posisi
        const npcY = Math.random() * 50; 
        npcXPos += 300 + Math.random() * 200; // Jarak antar NPC
        
        npc.style.left = npcXPos + 'px';
        npc.style.bottom = (20 + npcY) + 'px';

        // Balon Chat NPC
        const npcChat = document.createElement('div');
        npcChat.className = 'chat-bubble';
        npcChat.innerText = `Halo, aku ${char}! 👋`;
        npc.appendChild(npcChat);

        uiElements.entities.appendChild(npc);
        gameData.npcs.push({ el: npc, x: npcXPos, y: npcY, chat: npcChat, name: char });
    });

    // Mulai Game Loop
    requestAnimationFrame(gameLoop);
}

export function gameLoop() {
    let moved = false;

    // Update Posisi
    if (state.keys.left) { state.x -= state.speed; state.direction = -1; moved = true; }
    if (state.keys.right) { state.x += state.speed; state.direction = 1; moved = true; }
    if (state.keys.up && state.y < 150) { state.y += state.speed * 0.7; moved = true; } // Limit gerak ke atas (kedalaman)
    if (state.keys.down && state.y > 0) { state.y -= state.speed * 0.7; moved = true; } // Limit lantai

    // Batas dunia kiri (kamar tidur)
    if (state.x < 50) state.x = 50;
    // Batas dunia kanan (halaman mobil)
    if (state.x > 3300) state.x = 3300; 

    // Render Player
    gameData.player.style.left = state.x + 'px';
    gameData.player.style.bottom = (20 + state.y) + 'px';
    
    // Animasi jalan & hadap
    if (moved) {
        if (!state.isWalking) {
            gameData.player.classList.add('walking');
            state.isWalking = true;
        }
    } else {
        if (state.isWalking) {
            gameData.player.classList.remove('walking');
            state.isWalking = false;
        }
    }
    
    // Flip gambar
    if (state.direction === -1) {
        gameData.player.classList.add('flip-x');
        // Unflip balon chat
        document.getElementById('player-chat').style.transform = "translateX(-50%) scaleX(-1)";
    } else {
        gameData.player.classList.remove('flip-x');
        document.getElementById('player-chat').style.transform = "translateX(-50%) scaleX(1)";
    }

    // Camera Follow (Geser dunia)
    const screenCenter = window.innerWidth / 2;
    let cameraX = screenCenter - state.x;
    
    // Limit camera panning
    if (cameraX > 0) cameraX = 0; // Kiri mentok
    // Max world width ~3500px
    const maxScroll = -(3500 - window.innerWidth);
    if (cameraX < maxScroll) cameraX = maxScroll;
    
    uiElements.world.style.left = cameraX + 'px';

    checkProximity();

    requestAnimationFrame(gameLoop);
}

export function checkProximity() {
    let found = null;
    const interactRange = 150;

    // Cek jarak dengan NPC
    for (let npc of gameData.npcs) {
        const dx = Math.abs(state.x - npc.x);
        if (dx < interactRange) {
            found = { type: 'npc', data: npc };
            break; // Cukup temukan satu terdekat
        }
    }

    // Cek jarak dengan objek
    if (!found) {
        for (let obj of gameData.interactables) {
            const rect = obj.el.getBoundingClientRect();
            const playerRect = gameData.player.getBoundingClientRect();
            
            // Jarak pusat ke pusat secara horizontal (X)
            const objCenter = rect.left + rect.width / 2;
            const playerCenter = playerRect.left + playerRect.width / 2;
            
            if (Math.abs(playerCenter - objCenter) < interactRange) {
                found = { type: 'object', data: obj };
                break;
            }
        }
    }

    if (found) {
        if (gameData.currentFocus !== found.data) {
            gameData.currentFocus = found.data;
            gameData.currentFocus.type = found.type;
            uiElements.actionBtn.style.display = 'flex';
        }
    } else {
        if (gameData.currentFocus) {
            gameData.currentFocus = null;
            uiElements.actionBtn.style.display = 'none';
            // Sembunyikan bubble NPC jika menjauh
            gameData.npcs.forEach(n => n.chat.classList.remove('show'));
        }
    }
}

export function triggerAction() {
    if (!gameData.currentFocus) return;

    if (gameData.currentFocus.type === 'npc') {
        // Tampilkan chat NPC
        gameData.currentFocus.chat.classList.add('show');
        // Sembunyikan otomatis setelah 3 detik
        setTimeout(() => {
            if (gameData.currentFocus && gameData.currentFocus.chat) {
                gameData.currentFocus.chat.classList.remove('show');
            }
        }, 3000);
    } else if (gameData.currentFocus.type === 'object') {
        showPlayerChat(gameData.currentFocus.msg);
        
        // Animasi khusus TV
        if (gameData.currentFocus.action === 'tv') {
            const tv = uiElements.tv;
            if (tv.classList.contains('tv-on')) {
                tv.classList.remove('tv-on');
                tv.innerHTML = `<span class="text-white font-bold text-lg">TV Layar Datar</span>`;
                tv.className = "furniture interactable absolute top-20 left-1/2 -translate-x-1/2 w-64 h-36 bg-gray-800 border-4 border-gray-900 rounded-xl shadow-lg flex items-center justify-center";
            } else {
                tv.classList.add('tv-on');
                tv.className = "furniture interactable absolute top-20 left-1/2 -translate-x-1/2 w-64 h-36 bg-blue-300 border-4 border-white rounded-xl shadow-[0_0_30px_rgba(59,130,246,0.8)] flex items-center justify-center overflow-hidden";
                tv.innerHTML = `<div class="w-full h-full bg-[url('https://placehold.co/300x150/3b82f6/ffffff?text=Kuromi+Movie')] bg-cover animate-pulse"></div>`;
            }
        }
    }
}

export function showPlayerChat(msg) {
    const bubble = document.getElementById('player-chat');
    bubble.innerText = msg;
    bubble.classList.add('show');
    setTimeout(() => {
        bubble.classList.remove('show');
    }, 3000);
}
