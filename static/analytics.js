let isTyping = false;

function typeText(element, text, speed = 20) {
    if (isTyping) return;
    isTyping = true;
    element.textContent = "";
    let i = 0;

    const interval = setInterval(() => {
        element.textContent += text.charAt(i);
        element.scrollTop = element.scrollHeight; // автоскролл
        i++;
        if (i >= text.length) {
            clearInterval(interval);
            isTyping = false;
        }
    }, speed);
}

async function startAnalytics() {
    const resultDiv = document.getElementById("analyticsResult");
    resultDiv.innerHTML = `<span class="loading">⏳ Генерируем аналитику...</span>`;

    try {
        const res = await fetch("/analytics"); // <-- маршрут к бекенду
        if (!res.ok) throw new Error(`Ошибка ${res.status}`);

        const data = await res.json();
        console.log("Ответ от бекенда:", data); // для отладки

        // Берём текст из ключа report
        const text = data.report || JSON.stringify(data, null, 2);
        typeText(resultDiv, text, 20);

    } catch (err) {
        console.error(err);
        resultDiv.textContent = "❌ Ошибка при получении аналитики.";
    }
}

document.getElementById("startAnalyticsBtn").addEventListener("click", startAnalytics);
