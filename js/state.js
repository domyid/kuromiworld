export const characters = ['kuromi', 'romina', 'koni', 'gareco', 'nyanmi', 'chumi', 'konmi', 'wanmi', 'bako', 'collimo', 'baku'];

export const state = {
    x: 200,
    y: 0,
    speed: 5,
    isWalking: false,
    direction: 1,
    keys: { up: false, down: false, left: false, right: false }
};

export const gameData = {
    player: null,
    npcs: [],
    interactables: [],
    currentFocus: null,
    isDarkMode: false
};

export const uiElements = {
    startScreen: document.getElementById('start-screen'),
    charSelect: document.getElementById('character-selection'),
    world: document.getElementById('world'),
    entities: document.getElementById('entities-container'),
    actionBtn: document.getElementById('action-btn'),
    tv: document.getElementById('tv-obj'),
    lampuBtn: document.getElementById('lampu-btn')
};
