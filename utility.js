document.addEventListener("DOMContentLoaded", () => {
    const images = document.querySelectorAll('.slideshow-container img');
    const prevButton = document.querySelector('.slideshow-button.left');
    const nextButton = document.querySelector('.slideshow-button.right');
    const indicatorContainer = document.querySelector('.indicator-container');
    let currentIndex = 0;

    // インジケーターを生成
    const createIndicators = () => {
        images.forEach((_, index) => {
            const indicator = document.createElement('div');
            indicator.classList.add('indicator');
            if (index === currentIndex) {
                indicator.classList.add('active');
            }
            indicatorContainer.appendChild(indicator);

            // インジケータークリックでスライド切り替え
            indicator.addEventListener('click', () => {
                changeSlide(index);
            });
        });
    };

    // インジケーターを更新
    const updateIndicators = () => {
        const indicators = document.querySelectorAll('.indicator');
        indicators.forEach((indicator, index) => {
            if (index === currentIndex) {
                indicator.classList.add('active');
            } else {
                indicator.classList.remove('active');
            }
        });
    };

    const changeSlide = (index) => {
        images[currentIndex].classList.remove('active');
        currentIndex = (index + images.length) % images.length;
        images[currentIndex].classList.add('active');
        updateIndicators();
    };

    // ボタンのクリックイベント
    prevButton.addEventListener('click', () => {
        changeSlide(currentIndex - 1);
    });

    nextButton.addEventListener('click', () => {
        changeSlide(currentIndex + 1);
    });

    // 初期化
    createIndicators();
});