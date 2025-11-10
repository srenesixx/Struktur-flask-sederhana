document.addEventListener("DOMContentLoaded", () => {
  const footer = document.querySelector(".footer");
  for (let i = 0; i < 10; i++) {
    let bubble = document.createElement("span");
    bubble.classList.add("bubble");
    bubble.style.left = Math.random() * 100 + "%";
    bubble.style.animationDelay = Math.random() * 5 + "s";
    footer.appendChild(bubble);
  }
});
