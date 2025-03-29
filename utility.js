document.addEventListener("DOMContentLoaded", () => {
    const images = document.querySelectorAll('.slideshow-container img');
    const prevButton = document.querySelector('.slideshow-button.left');
    const nextButton = document.querySelector('.slideshow-button.right');
    const indicatorContainer = document.querySelector('.indicator-container');
    let currentIndex = 0;
    // パスワード保護のスクリプト
    const correctPassword = "my0601"; // 正しいパスワードを設定
    const passwordScreen = document.getElementById("password-screen");
    const mainContent = document.getElementById("main-content");
    const passwordInput = document.getElementById("password-input");
    const passwordSubmit = document.getElementById("password-submit");
    const passwordError = document.getElementById("password-error");

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

    passwordSubmit.addEventListener("click", () => {
        const enteredPassword = passwordInput.value;
        if (enteredPassword === correctPassword) {
            passwordScreen.style.display = "none"; // パスワード画面を非表示
            mainContent.style.display = "block"; // メインコンテンツを表示
        } else {
            passwordError.style.display = "block"; // エラーメッセージを表示
        }
    });

    // 外部HTMLファイルを読み込むスクリプト
    fetch('message.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('message-container').innerHTML = data;
        })
        .catch(error => console.error('メッセージの読み込みに失敗しました:', error));

    fetch('link.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('link-container').innerHTML = data;
        })
        .catch(error => console.error('リンクの読み込みに失敗しました:', error));
});