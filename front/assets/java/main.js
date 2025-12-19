// Функция для получения CSRF-токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Переменные для хранения доступных частей
let availableHeads = [];
let availableBodies = [];

// Загрузка доступных частей с сервера
async function loadAvailableParts() {
    try {
        const response = await fetch('/api/available_parts/');
        const data = await response.json();
        availableHeads = data.heads;
        availableBodies = data.bodies;
    } catch (error) {
        console.error("Ошибка загрузки доступных частей:", error);
    }
}

// Обновление выпадающего списка голов
function updateHeadSelect() {
    const headSelect = document.querySelector('[name="head"]');
    if (headSelect) {
        headSelect.innerHTML = '';
        availableHeads.forEach(head => {
            const option = document.createElement('option');
            option.value = head.id;
            option.textContent = head.name;
            headSelect.appendChild(option);
        });
    }
}

// Обновление выпадающего списка тел
function updateBodySelect() {
    const bodySelect = document.querySelector('[name="body"]');
    if (bodySelect) {
        bodySelect.innerHTML = '';
        availableBodies.forEach(body => {
            const option = document.createElement('option');
            option.value = body.id;
            option.textContent = body.name;
            bodySelect.appendChild(option);
        });
    }
}

// Обновление изображения головы
function updateHeadImage(headId) {
    const selectedHead = availableHeads.find(head => head.id == headId);
    if (selectedHead) {
        const headImage = document.getElementById('cat-head');
        if (headImage) {
            headImage.src = selectedHead.image;
        }
    }
}

// Обновление изображения тела
function updateBodyImage(bodyId) {
    const selectedBody = availableBodies.find(body => body.id == bodyId);
    if (selectedBody) {
        const bodyImage = document.getElementById('cat-body');
        if (bodyImage) {
            bodyImage.src = selectedBody.image;
        }
    }
}

// Сохранение кота
async function saveCat() {
    const selectedHeadId = document.querySelector('[name="head"]:checked')?.value;
    const selectedBodyId = document.querySelector('[name="body"]:checked')?.value;

    if (!selectedHeadId || !selectedBodyId) {
        alert("Пожалуйста, выберите голову и тело для кота.");
        return;
    }

    try {
        const response = await fetch('/api/save_cat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                head: selectedHeadId,
                body: selectedBodyId,
            }),
        });

        if (response.ok) {
            alert("Котик успешно сохранён!");
        } else {
            alert("Ошибка сохранения котика.");
        }
    } catch (error) {
        console.error("Ошибка:", error);
        alert("Произошла ошибка при сохранении.");
    }
}

// Обработчики событий для переключения частей
function bindArrows() {
    const prevHeadBtn = document.querySelector('.head-arrow.arrow-btn--left');
    const nextHeadBtn = document.querySelector('.head-arrow.arrow-btn--right');
    const prevBodyBtn = document.querySelector('.body-arrow.arrow-btn--left');
    const nextBodyBtn = document.querySelector('.body-arrow.arrow-btn--right');

    if (prevHeadBtn && nextHeadBtn) {
        let currentHeadIndex = 0;
        prevHeadBtn.addEventListener('click', () => {
            currentHeadIndex = (currentHeadIndex - 1 + availableHeads.length) % availableHeads.length;
            const selectedHeadId = availableHeads[currentHeadIndex].id;
            document.querySelector(`[name="head"][value="${selectedHeadId}"]`).checked = true;
            updateHeadImage(selectedHeadId);
        });

        nextHeadBtn.addEventListener('click', () => {
            currentHeadIndex = (currentHeadIndex + 1) % availableHeads.length;
            const selectedHeadId = availableHeads[currentHeadIndex].id;
            document.querySelector(`[name="head"][value="${selectedHeadId}"]`).checked = true;
            updateHeadImage(selectedHeadId);
        });
    }

    if (prevBodyBtn && nextBodyBtn) {
        let currentBodyIndex = 0;
        prevBodyBtn.addEventListener('click', () => {
            currentBodyIndex = (currentBodyIndex - 1 + availableBodies.length) % availableBodies.length;
            const selectedBodyId = availableBodies[currentBodyIndex].id;
            document.querySelector(`[name="body"][value="${selectedBodyId}"]`).checked = true;
            updateBodyImage(selectedBodyId);
        });

        nextBodyBtn.addEventListener('click', () => {
            currentBodyIndex = (currentBodyIndex + 1) % availableBodies.length;
            const selectedBodyId = availableBodies[currentBodyIndex].id;
            document.querySelector(`[name="body"][value="${selectedBodyId}"]`).checked = true;
            updateBodyImage(selectedBodyId);
        });
    }
}

// Существующий код для каталога, навигации, карусели, OTP, вкладок
const catalogToggle = document.querySelector('.catalog-toggle');
const header = document.querySelector('.site-header');

if (catalogToggle) {
    const toggleButton = catalogToggle.querySelector('button');
    toggleButton?.addEventListener('click', () => {
        catalogToggle.classList.toggle('open');
    });

    document.addEventListener('click', (event) => {
        if (!catalogToggle.contains(event.target)) {
            catalogToggle.classList.remove('open');
        }
    });
}

const navLinks = document.querySelectorAll('[data-scroll-to]');
navLinks.forEach((link) => {
    link.addEventListener('click', (event) => {
        event.preventDefault();
        const targetId = link.getAttribute('data-scroll-to');
        const target = document.querySelector(targetId);
        if (target) {
            const offset = header ? header.offsetHeight + 12 : 0;
            const top = target.getBoundingClientRect().top + window.scrollY - offset;
            window.scrollTo({top, behavior: 'smooth'});
        }
    });
});

const carousel = document.querySelector('.showcase-slider');
if (carousel) {
    let isDown = false;
    let startX;
    let scrollLeft;

    carousel.addEventListener('mousedown', (e) => {
        isDown = true;
        carousel.classList.add('is-grabbing');
        startX = e.pageX - carousel.offsetLeft;
        scrollLeft = carousel.scrollLeft;
    });

    carousel.addEventListener('mouseleave', () => {
        isDown = false;
        carousel.classList.remove('is-grabbing');
    });

    carousel.addEventListener('mouseup', () => {
        isDown = false;
        carousel.classList.remove('is-grabbing');
    });

    carousel.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - carousel.offsetLeft;
        const walk = (x - startX) * 1.4;
        carousel.scrollLeft = scrollLeft - walk;
    });
}

const otpInputs = document.querySelectorAll('.otp-inputs input');
otpInputs.forEach((input, index) => {
    input.addEventListener('input', () => {
        input.value = input.value.replace(/[^0-9]/g, '');
        if (input.value && index < otpInputs.length - 1) {
            otpInputs[index + 1].focus();
        }
    });

    input.addEventListener('keydown', (event) => {
        if (event.key === 'Backspace' && !input.value && index > 0) {
            otpInputs[index - 1].focus();
        }
    });
});

const tabs = document.querySelectorAll('[data-tab-target]');
const tabPanels = document.querySelectorAll('[data-tab-panel]');

tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
        const targetId = tab.getAttribute('data-tab-target');

        tabs.forEach((btn) => btn.classList.remove('active'));
        tabPanels.forEach((panel) => {
            if (panel.getAttribute('data-tab-panel') === targetId) {
                panel.style.display = 'grid';
            } else {
                panel.style.display = 'none';
            }
        });

        tab.classList.add('active');
    });
});

if (tabPanels.length > 0) {
    tabPanels.forEach((panel, index) => {
        panel.style.display = index === 0 ? 'grid' : 'none';
    });
}

// Логика конструктора котов
const builderControls = document.querySelector('.builder-controls');
if (builderControls) {
    const builderAssets = {
        body: {
            cream: {body: '#body-1', pattern: '#stripes'},
            violet: {body: '#body-2', pattern: '#spots'},
            mint: {body: '#body-3', pattern: null},
        },
        face: {
            smile: {head: '#head-1', eyes: '#eyes-1', muzzle: '#muzzle-1', whiskers: '#whisk-1', image: null},
            dream: {head: '#head-2', eyes: '#eyes-2', muzzle: '#muzzle-2', whiskers: '#whisk-2', image: null},
            pixel: {head: '#head-3', eyes: '#eyes-3', muzzle: '#muzzle-1', whiskers: '#whisk-1', image: null},
            legend: {head: null, eyes: null, muzzle: null, whiskers: null, image: 'legend'},
        },
        tail: {
            classic: '#tail-1',
            flare: '#tail-2',
            soft: '#tail-3',
        },
    };

    const spritePath = 'images/cats-sprite.svg';

    const bodyUse = document.getElementById('builder-body');
    const patternUse = document.getElementById('builder-pattern');
    const headUse = document.getElementById('builder-head');
    const eyesUse = document.getElementById('builder-eyes');
    const muzzleUse = document.getElementById('builder-muzzle');
    const whiskersUse = document.getElementById('builder-whiskers');
    const tailUse = document.getElementById('builder-tail');
    const faceImages = new Map();

    document.querySelectorAll('[data-face-image]').forEach((node) => {
        const key = node.getAttribute('data-face-image');
        if (key) {
            faceImages.set(key, node);
        }
    });

    const showFaceImage = (imageKey) => {
        faceImages.forEach((node, key) => {
            node.style.display = key === imageKey ? '' : 'none';
        });
    };

    const setUseHref = (element, symbolId) => {
        if (!element) return;
        if (symbolId) {
            element.setAttribute('href', `${spritePath}${symbolId}`);
            element.style.display = '';
        } else {
            element.removeAttribute('href');
            element.style.display = 'none';
        }
    };

    const applyFaceSelection = (value) => {
        const config = builderAssets.face[value];
        if (!config) {
            showFaceImage(null);
            return;
        }

        const {head, eyes, muzzle, whiskers, image} = config;
        setUseHref(headUse, head);
        setUseHref(eyesUse, eyes);
        setUseHref(muzzleUse, muzzle);
        setUseHref(whiskersUse, whiskers);
        showFaceImage(image ?? null);
    };

    builderControls.addEventListener('change', (event) => {
        const target = event.target;
        if (!(target instanceof HTMLInputElement) || target.type !== 'radio') {
            return;
        }

        const part = target.name;
        const value = target.value;

        switch (part) {
            case 'body':
                if (builderAssets.body[value]) {
                    const {body, pattern} = builderAssets.body[value];
                    setUseHref(bodyUse, body);
                    setUseHref(patternUse, pattern);
                }
                break;
            case 'face':
                applyFaceSelection(value);
                break;
            case 'tail':
                if (builderAssets.tail[value]) {
                    setUseHref(tailUse, builderAssets.tail[value]);
                }
                break;
            default:
                break;
        }
    });

    const initialFace = builderControls.querySelector('input[name="face"]:checked');
    if (initialFace instanceof HTMLInputElement) {
        applyFaceSelection(initialFace.value);
    } else {
        showFaceImage(null);
    }
}

// Инициализация
document.addEventListener('DOMContentLoaded', async () => {
    await loadAvailableParts();
    updateHeadSelect();
    updateBodySelect();
    bindArrows();

    // Устанавливаем начальные изображения
    if (availableHeads.length > 0) {
        const initialHeadId = availableHeads[0].id;
        document.querySelector(`[name="head"][value="${initialHeadId}"]`).checked = true;
        updateHeadImage(initialHeadId);
    }

    if (availableBodies.length > 0) {
        const initialBodyId = availableBodies[0].id;
        document.querySelector(`[name="body"][value="${initialBodyId}"]`).checked = true;
        updateBodyImage(initialBodyId);
    }
});
