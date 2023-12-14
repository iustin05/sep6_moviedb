const texts = ["Entertainment", "New Genres", "Family Time", "Movie Night", "Fun"].sort(() => Math.random() - 0.5);
    let textIndex = 0;
    const textElement = document.getElementById("text");

    function changeText() {
        textElement.innerHTML = texts[textIndex];
        textIndex = (textIndex + 1) % texts.length;
    }

    setInterval(changeText, 2500);

    const emojis = ["😀", "😃", "😄", "😁", "😆", "😅", "😂","🎥", "🍿", "🎬", "📽️", "🎞️", "🎦", "🎫", "🎭", "🎦", "🎟️"];
    const emojiContainer = document.getElementById("emoji-container");

    function addEmoji() {
        const emoji = document.createElement("div");
        emoji.className = "emoji";
    emoji.textContent = emojis[Math.floor(Math.random() * emojis.length)];
    emoji.style.left = Math.random() * 100 + "%";
    emoji.style.top = Math.random() * 100 + "%";
    emojiContainer.appendChild(emoji);

    setTimeout(function() {
        emoji.hidden = true;
    }, 8000);

    setTimeout(function() {
        emojiContainer.removeChild(emoji);
    }, 10000);
}

setInterval(addEmoji, 1000);