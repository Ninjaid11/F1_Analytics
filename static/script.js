async function loadPilots() {
    const response = await fetch("/pilots");
    const data = await response.json();

    const pilot1Select = document.getElementById("pilot1");
    const pilot2Select = document.getElementById("pilot2");

    data.forEach(pilot => {
        const name = `${pilot.name} ${pilot.surname}`;
        const option1 = new Option(name, name);
        const option2 = new Option(name, name);
        pilot1Select.add(option1);
        pilot2Select.add(option2);
    });
}

// Функция для "печатающейся строки"
function typeText(element, text, speed = 20) {
    element.textContent = "";  // очищаем перед началом
    let i = 0;

    const interval = setInterval(() => {
        element.textContent += text.charAt(i);
        i++;

        element.scrollTop = element.scrollHeight;
        // можно добавить кастомное поведение, если нужно
        if (i >= text.length) clearInterval(interval);
    }, speed);
}

async function comparePilots() {
    const pilot1 = document.getElementById("pilot1").value;
    const pilot2 = document.getElementById("pilot2").value;
    const resultDiv = document.getElementById("result");

    if (!pilot1 || !pilot2) {
        resultDiv.textContent = "⚠️ Пожалуйста, выберите обоих пилотов.";
        return;
    }

    resultDiv.innerHTML = `<span class="loading">⏳ Анализируем пилотов...</span>`;

    try {
        const res = await fetch(`/compare?pilot1=${encodeURIComponent(pilot1)}&pilot2=${encodeURIComponent(pilot2)}`);
        const data = await res.json();

        // вывод по буквам
        const text = `🏁 ${pilot1} vs ${pilot2}\n\n${data.report || "Нет данных."}`;
        typeText(resultDiv, text, 20); // 20ms на букву
    } catch (err) {
        resultDiv.textContent = "❌ Ошибка при получении данных.";
    }
}

document.getElementById("compareBtn").addEventListener("click", comparePilots);
loadPilots();