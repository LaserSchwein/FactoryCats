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
            window.scrollTo({ top, behavior: 'smooth' });
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

/* --- СТАРАЯ ЛОГИКА (ЕСЛИ ОНА ВАМ НУЖНА ДЛЯ ДРУГОГО КОНСТРУКТОРА) --- */
const builderControls = document.querySelector('.builder-controls');
if (builderControls) {
    const builderAssets = {
        body: {
            cream: { body: '#body-1', pattern: '#stripes' },
            violet: { body: '#body-2', pattern: '#spots' },
            mint: { body: '#body-3', pattern: null },
        },
        face: {
            smile: { head: '#head-1', eyes: '#eyes-1', muzzle: '#muzzle-1', whiskers: '#whisk-1', image: null },
            dream: { head: '#head-2', eyes: '#eyes-2', muzzle: '#muzzle-2', whiskers: '#whisk-2', image: null },
            pixel: { head: '#head-3', eyes: '#eyes-3', muzzle: '#muzzle-1', whiskers: '#whisk-1', image: null },
            legend: { head: null, eyes: null, muzzle: null, whiskers: null, image: 'legend' },
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

        const { head, eyes, muzzle, whiskers, image } = config;
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
                    const { body, pattern } = builderAssets.body[value];
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

/* --- НОВАЯ ЛОГИКА ДЛЯ builder.html (СТРЕЛКИ) --- */
/* Проверяем, есть ли на странице элементы конструктора, чтобы не вызывать ошибок */
const catHeadImg = document.getElementById("cat-head");
const catBodyImg = document.getElementById("cat-body");

if (catHeadImg && catBodyImg) {
    // Массивы с путями к изображениям
    const heads = [
        "../assets/images/head-1.png",
        "../assets/images/head-2.png",
        "../assets/images/head-3.png",
        "../assets/images/head-4.png",
        "../assets/images/head-5.png",
        "../assets/images/head-6.png",
        "../assets/images/head-7.png"
    ];

    const bodies = [
        "../assets/images/body-1.png",
        "../assets/images/body-2.png",
        "../assets/images/body-3.png",
        "../assets/images/body-4.png",
        "../assets/images/body-5.png",
        "../assets/images/body-6.png"
    ];

    let headIndex = 0;
    let bodyIndex = 0;

    function updateHead() {
        if(catHeadImg) catHeadImg.src = heads[headIndex];
    }

    function updateBody() {
        if(catBodyImg) catBodyImg.src = bodies[bodyIndex];
    }

    function nextHead() {
        headIndex = (headIndex + 1) % heads.length;
        updateHead();
    }

    function prevHead() {
        headIndex = (headIndex - 1 + heads.length) % heads.length;
        updateHead();
    }

    function nextBody() {
        bodyIndex = (bodyIndex + 1) % bodies.length;
        updateBody();
    }

    function prevBody() {
        bodyIndex = (bodyIndex - 1 + bodies.length) % bodies.length;
        updateBody();
    }

    // Привязка событий к кнопкам
    const headPrevBtn = document.querySelector('.head-arrow.arrow-btn--left');
    const headNextBtn = document.querySelector('.head-arrow.arrow-btn--right');
    const bodyPrevBtn = document.querySelector('.body-arrow.arrow-btn--left');
    const bodyNextBtn = document.querySelector('.body-arrow.arrow-btn--right');

    if (headPrevBtn) headPrevBtn.addEventListener('click', prevHead);
    if (headNextBtn) headNextBtn.addEventListener('click', nextHead);
    if (bodyPrevBtn) bodyPrevBtn.addEventListener('click', prevBody);
    if (bodyNextBtn) bodyNextBtn.addEventListener('click', nextBody);

    // Запуск при загрузке
    updateHead();
    updateBody();
}