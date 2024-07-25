const sentences = [
    "Explore our latest opportunities today!",
    "Start your career with us!",
    "Apply now and make a difference!"
];

let sentenceIndex = 0;
let charIndex = 0;
const typingTextElement = document.getElementById("typing-text");

function type() {
    if (charIndex < sentences[sentenceIndex].length) {
        typingTextElement.textContent += sentences[sentenceIndex].charAt(charIndex);
        charIndex++;
        setTimeout(type, 100);
    } else {
        setTimeout(erase, 2000); // Pause before erasing
    }
}

function erase() {
    if (charIndex > 0) {
        typingTextElement.textContent = sentences[sentenceIndex].substring(0, charIndex - 1);
        charIndex--;
        setTimeout(erase, 50);
    } else {
        sentenceIndex = (sentenceIndex + 1) % sentences.length;
        setTimeout(type, 1000); // Pause before typing next sentence
    }
}

document.addEventListener("DOMContentLoaded", function() {
    setTimeout(type, 1000); // Start typing after a short delay
});