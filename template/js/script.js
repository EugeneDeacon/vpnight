// Generate stars
function generateStars() {
    const nightSky = document.getElementById('nightSky');
    const numStars = 100;

    for (let i = 0; i < numStars; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.width = (Math.random() * 2 + 0.5) + 'px';
        star.style.height = star.style.width;
        star.style.opacity = Math.random() * 0.8 + 0.2;
        star.style.animationDuration = (2 + Math.random() * 3) + 's';
        nightSky.appendChild(star);
    }
}
// Generate shooting stars
function createShootingStar() {
    if (Math.random() > 0.1) {
        const nightSky = document.getElementById('nightSky');
        const shootingStar = document.createElement('div');
        shootingStar.className = 'shooting-star';
        shootingStar.style.left = Math.random() * 100 + '%';
        shootingStar.style.top = Math.random() * 30 + '%';

        const rotation = Math.random() * 60 + 15;
        shootingStar.style.transform = `rotate(${rotation}deg)`;

        nightSky.appendChild(shootingStar);

        // Remove after animation
        setTimeout(() => {
            if (shootingStar.parentNode) {
                nightSky.removeChild(shootingStar);
            }
        }, 4000);
    }
}

// Accordion functionality
function initAccordion() {
    const accordionItems = document.querySelectorAll('.accordion-item');

    accordionItems.forEach(item => {
        const trigger = item.querySelector('.accordion-trigger');

        trigger.addEventListener('click', () => {
            const isActive = item.classList.contains('active');

            // Close all items
            accordionItems.forEach(otherItem => {
                otherItem.classList.remove('active');
            });

            // Open clicked item if it wasn't active
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
}

// Download and share functions
function downloadApp(url) {
    window.location.href = url;
}

function shareApp(url) {

    window.location.href = url;
}

// Copy share link function
function copyShareLink() {
    const shareUrl = document.getElementById('shareUrl').textContent;
    const copyIcon = document.getElementById('copyIcon');

    if (navigator.clipboard) {
        navigator.clipboard.writeText(shareUrl).then(() => {
            // Change icon to checkmark
            copyIcon.className = 'fas fa-check';
            setTimeout(() => {
                copyIcon.className = 'fas fa-copy';
            }, 2000);
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = shareUrl;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);

        // Change icon to checkmark
        copyIcon.className = 'fas fa-check';
        setTimeout(() => {
            copyIcon.className = 'fas fa-copy';
        }, 2000);
    }
}

// Calculate subscription days
function updateSubscriptionInfo() {
    const subscriptionEndDate = new Date('2024-03-15');
    const currentDate = new Date();
    const timeDiff = subscriptionEndDate.getTime() - currentDate.getTime();
    const daysRemaining = Math.max(0, Math.ceil(timeDiff / (1000 * 3600 * 24)));

    document.getElementById('daysRemaining').textContent = daysRemaining;
    document.getElementById('subscriptionDate').textContent = subscriptionEndDate.toLocaleDateString('ru-RU');

    let label = 'дней осталось';
    if (daysRemaining === 1) {
        label = 'день остался';
    } else if (daysRemaining < 5) {
        label = 'дня осталось';
    }
    document.getElementById('daysLabel').textContent = label;
}

function generateExpiredDate() {
    const expireTimestamp = {{ user.expire }};

    // Проверяем, что дата валидна
    if (expireTimestamp && !isNaN(expireTimestamp)) {
        const date = new Date(expireTimestamp * 1000); // JS использует миллисекунды
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        document.getElementById('subscriptionDate').textContent = `${day}.${month}.${year}`;
    } else {

    }
}

function generateExpiredDays() {
  // Получаем дату окончания из шаблона (в секундах)
  const expireTimestamp = {{ user.expire if user.expire else 'null' }};

  const daysRemainingElement = document.getElementById('daysRemaining');
  const daysLabelElement = document.getElementById('daysLabel');

  // Если дата не установлена (бессрочно)
  if (expireTimestamp === null) {
    daysRemainingElement.textContent = '∞';
    daysLabelElement.textContent = 'бессрочно';
    daysLabelElement.style.color = '#2196F3';
    daysRemainingElement.style.color = '#2196F3';
    daysRemainingElement.style.fontWeight = 'bold';
    document.querySelector('.subscription-title').textContent = 'Статус подписки';
    return;
  }

  // Текущее время в секундах
  const now = Math.floor(Date.now() / 1000);

  // Разница в днях (округляем вверх, чтобы 1.2 дня = 2 дня)
  const diffInSeconds = expireTimestamp - now;
  const daysLeft = Math.ceil(diffInSeconds / (24 * 60 * 60));

  // Обновляем число
  daysRemainingElement.textContent = daysLeft > 0 ? daysLeft : '0';

  // Склонение: день, дня, дней
  let label;
  if (daysLeft === 1) {
    label = 'день остался';
  } else if (daysLeft >= 2 && daysLeft <= 4) {
    label = 'дня осталось';
  } else {
    label = 'дней осталось';
  }

  // Если подписка уже закончилась
  if (daysLeft <= 0) {
    daysRemainingElement.textContent = '0';
    label = 'подписка истекла';
  }

  // Устанавливаем текст
  daysLabelElement.textContent = label;
}


// Initialize everything
document.addEventListener('DOMContentLoaded', () => {
    generateStars();
    initAccordion();
    updateSubscriptionInfo();
    generateExpiredDate();
    generateExpiredDays();

    // Start shooting stars interval
    setInterval(createShootingStar, 3000);
});
