document.addEventListener("DOMContentLoaded", () => {
    const images = document.querySelectorAll('.slideshow-container img');
    const prevButton = document.querySelector('.slideshow-button.left');
    const nextButton = document.querySelector('.slideshow-button.right');
    let currentIndex = 0;

    const changeSlide = (index) => {
        images[currentIndex].classList.remove('active');
        currentIndex = (index + images.length) % images.length;
        images[currentIndex].classList.add('active');
    };

    // 自動スライド
    setInterval(() => {
        changeSlide(currentIndex + 1);
    }, 3000);

    // ボタンのクリックイベント
    prevButton.addEventListener('click', () => {
        changeSlide(currentIndex - 1);
    });

    nextButton.addEventListener('click', () => {
        changeSlide(currentIndex + 1);
    });
});