<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <title>Septic24 – Послуги асенізатора в Україні</title>
  <!-- Фіксація сторінки (заборона масштабування і скролла) -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

  <!-- Підключення шрифта Montserrat -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link 
    href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap"
    rel="stylesheet"
  >
  
  <!-- OpenLayers CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ol@7.3.0/dist/ol.css">
  
  <style>
    /* Сховати атрибуцію OpenStreetMap */
    .ol-attribution {
      display: none !important;
    }
    
    /* Відключаємо прокрутку головної сторінки */
    html, body {
      margin: 0;
      padding: 0;
      height: 100%;
      overflow: hidden;
      font-family: 'Montserrat', sans-serif;
      background: linear-gradient(135deg, #ffffff, #d0e8ff);
      color: #002050;
      transition: background 0.5s, color 0.5s;
    }

    /* Логотип на головній сторінці */
    #mainLogo {
      position: fixed;
      top: 5px;
      right: 10px;
      z-index: 10000;
    }
    #mainLogo img {
      width: 40px;
      height: auto;
      border-radius: 50%;
      object-fit: cover;
      background: transparent;
    }
    
    /* Іконки месенджерів у лівому куті */
    #socialIcons {
      position: fixed;
      top: 10px;
      left: 15px;
      z-index: 10000;
      display: flex;
      gap: 10px;
    }
    #socialIcons img {
      width: 30px;
      height: auto;
      filter: invert(38%) sepia(100%) saturate(5000%) hue-rotate(180deg) brightness(85%) contrast(105%);
    }
    
    /* Блок з номерами телефонів */
    #phoneNumbers {
      position: fixed;
      top: 10px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 10000;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    #phoneNumbers a {
      margin: 2px 0;
      text-decoration: none;
      color: #002050;
      font-weight: bold;
      font-size: 0.8rem;
    }
    
    /* Екран завантаження */
    .loader {
      position: fixed;
      top: 0; left: 0;
      width: 100vw;
      height: 100vh;
      background: linear-gradient(135deg, #f0f9ff, #d0e8ff);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      z-index: 99999;
      text-align: center;
    }
    .loader-logo-wrap {
      position: relative;
      width: 200px;
      height: 200px;
    }
    .loader-logo-wrap::before {
      content: "";
      position: absolute;
      top: 50%;
      left: 50%;
      width: 100%;
      height: 100%;
      transform: translate(-50%, -50%);
      border: 2px solid rgba(0, 96, 160, 0.2);
      border-top: 2px solid #0060a0;
      border-radius: 50%;
      animation: ringSpin 2s linear infinite;
    }
    @keyframes ringSpin {
      0%   { transform: translate(-50%, -50%) rotate(0deg); }
      100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    .loader-logo-wrap img {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 50%;
      z-index: 1;
      box-shadow: 0 0 20px #80d0ff;
    }
    /* Текст під завантажувачем – трохи опущений і світліший */
    .loader p {
      margin-top: 20px;
      font-weight: 700;
      color: #4F6D8F;
    }
    
    /* Основний контейнер – спочатку прихований, щоб не було видно головного меню до завантаження */
    .container {
      display: none;
      width: 100%;
      max-width: 1200px;
      margin: 0 auto;
      min-height: 100vh;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      padding: 120px 20px 20px 20px;
      box-sizing: border-box;
      text-align: center;
    }
    .animate {
      animation: fadeInUp 0.8s ease forwards;
    }
    @keyframes fadeInUp {
      from { transform: translateY(20px); opacity: 0; }
      to   { transform: translateY(0);     opacity: 1; }
    }
    
    /* Заголовок та опис */
    #title {
      font-size: 2rem;
      margin-bottom: 10px;
      font-weight: 700;
    }
    #mainImage {
      display: block;
      margin: 20px auto;
      max-width: 250px;
      width: 100%;
      height: auto;
    }
    /* Змінено: "вигребних" → "вигрібних" */
    #description {
      font-size: 1rem;
      line-height: 1.4;
      max-width: 700px;
      margin: 0 10px;
    }
    #boldLine {
      font-weight: 700;
      font-size: 1rem;
      margin: 10px 20px 0 20px;
    }
    
    /* Кнопки головного меню */
    .buttons {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 15px;
      margin-top: 20px;
      width: 100%;
      max-width: 300px;
    }
    .btn {
      width: 100%;
      padding: 12px 20px;
      font-weight: 700;
      font-size: 1.1rem;
      text-decoration: none;
      text-align: center;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      color: #fff;
      background: #0060a0;
      cursor: pointer;
      border-radius: 5px;
      border: none;
      display: inline-flex; 
      align-items: center; 
      justify-content: center;
    }
    .btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 0 5px #0060a0, 0 0 10px #0060a0;
    }
    .btn:active {
      transform: scale(0.95);
      box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
    }
    #btnOrder {
      box-shadow: 0 0 5px 1px #90EE90;
    }
    
    /* Стилізація модальних вікон */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0;
      width: 100vw; 
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 99998;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.5s ease;
      background: rgba(0, 0, 0, 0.7);
    }
    .modal-overlay.active {
      opacity: 1;
      pointer-events: auto;
    }
    .modal {
      position: relative;
      padding: 20px;
      border-radius: 8px;
      max-width: 300px;
      min-height: 400px;
      width: 90%;
      transform: translateY(-20px);
      opacity: 0;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: flex-start;
      text-align: left;
      transition: transform 0.5s ease, opacity 0.5s ease;
      background: linear-gradient(135deg, #ffffff, #d0e8ff);
      color: #002050;
      border: 2px solid #0060a0;
      box-shadow: 0 0 5px #0060a0, 0 0 10px #0060a0;
      max-height: 80vh;
      overflow-y: auto;
    }
    .modal.active {
      transform: translateY(0);
      opacity: 1;
    }
    .modal .modal-close {
      position: absolute;
      top: 10px;
      right: 10px;
      cursor: pointer;
      font-size: 2rem;
      line-height: 1;
      color: #002050;
    }
    
    /* Про нас */
    #modalAbout {
      max-width: 320px;
      text-align: center;
    }
    
    /* Слайдер (Послуги) */
    .slider-container {
      position: relative;
      overflow: hidden;
      width: 100%;
      margin-top: 10px;
      min-height: 300px;
      padding-bottom: 40px;
    }
    .slider {
      display: flex;
      transition: transform 0.3s ease;
      height: 100%;
    }
    .service-card {
      flex: 0 0 100%;
      margin: 0;
      border-radius: 6px;
      padding: 15px;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      min-height: 550px;
      margin-top: 30px;
    }
    .service-card h3 {
      margin: 0 0 10px 0;
      font-weight: 700;
    }
    .service-card img {
      max-width: 100%;
      height: auto;
      margin: 10px 0;
      border-radius: 4px;
    }
    .service-card p {
      font-size: 0.95rem;
      margin: 2px 5px;
      text-align: justify;
      line-height: 1.2;
    }
    
    /* Кнопки "Оберіть послугу" (Крок 1) */
    #orderServicesButtons {
      padding-left: 10px;
    }
    #orderServicesButtons .btn {
      display: inline-flex;
      align-items: center;
      justify-content: flex-start;
      width: 100%;
      min-height: 60px;
      margin-bottom: 10px;
      white-space: nowrap;
    }
    
    /* Кнопки вибору областей (Крок 2) */
    #regionButtons {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      width: 100%;
      max-width: 320px;
      margin: 0 auto;
    }
    #regionButtons .btn {
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 0.85rem;
      text-align: center;
      white-space: nowrap;
      min-height: 35px;
      padding: 6px 8px;
    }
    
    /* Додаткові стилі для Кроку 1.5 */
    #orderStep1_5_tubes, #orderStep1_5_capacity {
      display: none; 
      text-align: center; 
      width: 100%;
      box-sizing: border-box;
      margin-top: 50px;
    }
    
    /* Збільшені стилі для range-інпутів */
    input[type="range"].big {
      -webkit-appearance: none;
      appearance: none;
      width: 80%;
      margin: 0 auto;
      height: 12px;
      border-radius: 4px;
      background: #ccc;
      outline: none;
      cursor: pointer;
    }
    input[type="range"].big:focus {
      outline: none;
    }
    input[type="range"].big::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 24px; 
      height: 24px; 
      border-radius: 50%;
      background: #0060a0;
      border: none;
      cursor: pointer;
      box-shadow: none;
    }
    input[type="range"].big::-moz-range-thumb {
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: #0060a0;
      border: none;
      cursor: pointer;
    }

    /* Стилі для блоку з картою */
    #olMap {
      width: 100%;
      height: 300px;
      border-radius: 8px;
      margin-top: 10px;
    }

    /* Збільшений input для адреси з зеленою рамкою */
    #addressInput {
      width: 90%;
      padding: 10px;
      font-size: 1.1rem;
      border: 1px solid green;
    }

    /* Окно для вводу імені та номера телефону – збільшені поля з зеленим тонким контуром */
    .modal-user-data input {
      width: 90%;
      padding: 10px;
      font-size: 1.1rem;
      border: 1px solid green;
      margin: 10px auto;
      text-align: center;
      display: block;
    }
    
    /* Окно для вводу імені та номера телефону */
    .modal-overlay#modalOverlayUserData {
    }
    .modal-user-data {
      position: relative;
      padding: 20px;
      border-radius: 8px;
      max-width: 300px;
      width: 90%;
      min-height: 400px;
      transform: translateY(-20px);
      opacity: 0;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: flex-start;
      text-align: left;
      transition: transform 0.5s ease, opacity 0.5s ease;
      background: linear-gradient(135deg, #ffffff, #d0e8ff);
      color: #002050;
      border: 2px solid #0060a0;
      box-shadow: 0 0 5px #0060a0, 0 0 10px #0060a0;
      max-height: 80vh;
      overflow-y: auto;
    }
    .modal-user-data.active {
      transform: translateY(0);
      opacity: 1;
    }
    
    /* Нове модальне вікно для "Мої замовлення" */
    #modalMyOrders {
      max-width: 320px;
      text-align: center;
    }
    
    /* Медіа-запити для адаптивності */
    @media (max-width: 600px) {
      #title { font-size: 1.5rem; }
      #description { font-size: 0.9rem; }
      .btn { font-size: 1rem; padding: 10px; }
      .container { padding: 120px 10px 10px 10px; }
      #orderStep1 {
        align-items: center;
        text-align: center;
      }
      #orderServicesButtons .btn span {
        flex: unset;
        text-align: center !important;
        margin: 0 auto;
      }
    }
  </style>
</head>
<body>
  <!-- Іконки месенджерів (Telegram та Viber) -->
  <div id="socialIcons">
    <a href="https://t.me/Septic24_ua" target="_blank"><img src="https://i.ibb.co/r24wtsvm/61-1.png" alt="Telegram"></a>
    <a href="viber://chat?number=+380980099686" target="_blank"><img src="https://i.ibb.co/PvmNdLvN/62-1.png" alt="Viber"></a>
  </div>

  <!-- Блок з номерами телефонів -->
  <div id="phoneNumbers">
    <a href="tel:+380980099686" target="_blank">+38 (098) 0099-686</a>
    <a href="tel:+380662960008" target="_blank">+38 (066) 296-0008</a>
  </div>
  
  <!-- Логотип -->
  <div id="mainLogo">
    <a href="https://septic24.com.ua">
      <img src="https://i.ibb.co/BH3bjrPP/IMG-9356.jpg" alt="Logo">
    </a>
  </div>
  
  <!-- Екран завантаження -->
  <div class="loader" id="loader">
    <div class="loader-logo-wrap">
      <img src="https://i.ibb.co/3Q3LXDk/IMG-9356.png" alt="Loader Logo">
    </div>
    <p>Сервіс каналізаційних послуг</p>
  </div>
  
  <!-- Основний контейнер (зараз прихований) -->
  <div class="container">
    <h1 id="title">Послуги асенізатора по всій Україні</h1>
    <img id="mainImage" src="https://i.ibb.co/211q15HY/2025-03-25-171453.png" alt="Decorative Image">
    <!-- Змінено: "вигребних" → "вигрібних" -->
    <p id="description">
      Викачка вигрібних ям, викачка сливних ям і каналізацій, відкачка септиків та туалетів.
    </p>
    <p id="boldLine">
      Потрібен асенізатор?<br>
      Один клік — і ми вже на виїзді!
    </p>
    
    <!-- Кнопки головного меню -->
    <div class="buttons">
      <button class="btn" id="btnOrder">Замовити послугу</button>
      <button class="btn" id="btnMyOrders">Мої замовлення</button>
      <button class="btn" id="btnServices">Наші послуги</button>
      <button class="btn" id="btnAbout">Про компанію</button>
    </div>
  </div>
  
  <!-- Модальні вікна (Про компанію) -->
  <div class="modal-overlay" id="modalOverlayAbout">
    <div class="modal" id="modalAbout">
      <span class="modal-close" data-modal="modalOverlayAbout">&times;</span>
      <h2>Про компанію</h2>
      <p style="text-align: justify;">
        <strong>Septic24</strong> — це надійний сервіс виклику асенізатора по всій території України.
        Ми надаємо професійні послуги з відкачування вигрібних ям, септиків, каналізацій та вуличних туалетів
        у Києві, Дніпрі, Одесі та інших містах. Працюємо цілодобово, без вихідних, щоб забезпечити комфорт
        і чистоту у вашому домі чи на підприємстві.
      </p>
      <p style="text-align: justify; margin-top: 10px;">
        <strong>Наші переваги:</strong>
      </p>
      <ul style="padding-left: 20px; margin: 0; text-align: justify;">
        <li><strong>Безкоштовна консультація:</strong> Менеджери допоможуть обрати оптимальний варіант.</li>
        <li><strong>Зручне замовлення:</strong> Оформити можна по телефону або онлайн.</li>
        <li><strong>Підбір спецтехніки:</strong> Враховуємо об’єм вашої вигрібної ями чи септика.</li>
        <li><strong>Оперативність:</strong> Швидко реагуємо та виконуємо замовлення.</li>
        <li><strong>Якість:</strong> Повне відкачування відходів.</li>
        <li><strong>Прозорі ціни:</strong> Без прихованих платежів.</li>
        <li><strong>Екологічно:</strong> Безпечне вивезення та утилізація.</li>
      </ul>
      <p style="text-align: justify; margin-top: 10px;">
        Ми прагнемо бути вашим надійним помічником у вирішенні будь-яких питань, пов’язаних із вивозом стічних вод.
      </p>
    </div>
  </div>
  
  <!-- Окно Наші послуги -->
  <div class="modal-overlay" id="modalOverlayServices">
    <div class="modal" id="modalServices">
      <span class="modal-close" data-modal="modalOverlayServices">&times;</span>
      <div id="servicesSliderContainer" class="slider-container">
        <div id="servicesSlider" class="slider"></div>
      </div>
      <div style="width: 100%; display: flex; justify-content: center; align-items: center; gap: 20px; margin-top: 10px;">
         <button id="prevServiceBtn" class="btn" style="width: 80px; height: 30px;">&#8592;</button>
         <button id="nextServiceBtn" class="btn" style="width: 80px; height: 30px;">&#8594;</button>
      </div>
    </div>
  </div>
  
  <!-- Окно оформлення замовлення -->
  <div class="modal-overlay" id="modalOverlayOrder">
    <div class="modal" id="modalOrder">
      <span class="modal-close" data-modal="modalOverlayOrder">&times;</span>
      
      <!-- Крок 1: вибір послуги -->
      <div id="orderStep1">
        <h2>Оберіть послугу:</h2>
        <div id="orderServicesButtons" class="buttons" style="max-width: 300px;"></div>
      </div>
      
      <!-- Крок 1.5 для "Прочистка труб": параметри труб -->
      <div id="orderStep1_5_tubes">
        <h4 style="font-size: 1.2rem;">Яка довжина ваших труб в метрах</h4>
        <input 
          type="range" 
          id="lengthRange" 
          class="big"
          min="1" 
          max="400" 
          value="1" 
          oninput="document.getElementById('lengthValue').innerHTML = this.value + ' м';"
        >
        <div id="lengthValue" style="margin-bottom: 20px; font-size: 1.2rem;">1 м</div>
        <h4 style="font-size: 1.2rem;">Оберіть діаметр ваших труб в міліметрах</h4>
        <input 
          type="range" 
          id="diameterRange" 
          class="big"
          min="100" 
          max="900" 
          value="100" 
          oninput="document.getElementById('diameterValue').innerHTML = this.value + ' мм';"
        >
        <div id="diameterValue" style="margin-bottom: 20px; font-size: 1.2rem;">100 мм</div>
        <button class="btn" id="tubesNextBtn">Далі</button>
      </div>
      
      <!-- Крок 1.5 для інших послуг: параметри ємності -->
      <div id="orderStep1_5_capacity">
        <h4 style="font-size: 1.2rem;">Який об'єм вашої ємності в кубах?</h4>
        <input 
          type="range" 
          id="volumeRange" 
          class="big"
          min="1" 
          max="25" 
          value="1" 
          oninput="document.getElementById('volumeValue').innerHTML = this.value + ' м<sup>3</sup>';"
        >
        <div id="volumeValue" style="margin-bottom: 20px; font-size: 1.2rem;">1 м<sup>3</sup></div>
        <h4 style="font-size: 1.2rem;">Відстань від парковки до ємності</h4>
        <input 
          type="range" 
          id="distanceRange" 
          class="big"
          min="1" 
          max="70" 
          value="1" 
          oninput="document.getElementById('distanceValue').innerHTML = this.value + ' м';"
        >
        <div id="distanceValue" style="margin-bottom: 20px; font-size: 1.2rem;">1 м</div>
        <button class="btn" id="capacityNextBtn">Далі</button>
      </div>
      
      <!-- Крок 2: вибір області -->
      <div id="orderStep2" style="display: none; position: relative;">
        <div id="orderStep2Header" style="display: flex; justify-content: center; align-items: center; padding: 5px 0; margin-top: 0;">
          <h3 style="margin: 0; font-size: 1rem;">Оберіть область:</h3>
        </div>
        <div id="regionButtons"></div>
      </div>
    </div>
  </div>
  
  <!-- Окно карти -->
  <div class="modal-overlay" id="modalOverlayMap">
    <div class="modal" id="modalMap">
      <span class="modal-close" data-modal="modalOverlayMap">&times;</span>
      <p class="address-label">Вкажіть вашу адресу:</p>
      <div class="address-search-wrap">
        <input type="text" id="addressInput" placeholder="( Місто , вулиця , номер будинку )">
        <button id="searchAddressBtn">Пошук</button>
      </div>
      
      <p class="address-label" style="position: relative;">
        Або позначте місце подачі асенізатора на карті:
      </p>
      
      <div id="olMap"></div>
      
      <!-- Додаткові кнопки з додатковим відступом -->
      <button class="btn" id="getGeoBtn" style="display:block; margin-bottom:10px;">Моя геопозиція</button>
      <button class="btn" id="cancelLocationBtn" style="display:none; margin-bottom:10px;">Скасувати</button>
      <button class="btn" id="confirmLocationBtn" style="display:block;">Підтвердити</button>
      
      <div id="mapLoader">
        <div class="spinner"></div>
      </div>
    </div>
  </div>
  
  <!-- Окно для вводу імені та номера телефону -->
  <div class="modal-overlay" id="modalOverlayUserData">
    <div class="modal-user-data" style="max-width: 300px;" id="modalUserData">
      <h3 style="font-size:1.5rem;">Заповніть форму, і ми швидко зв'яжемось з Вами</h3>
      <input type="text" id="userName" placeholder="Введіть ваше ім'я">
      <input type="text" id="userPhone" value="+38 (___)___-__-__" placeholder="+38 (___)___-__-__">
      <button class="btn" id="confirmOrderBtn" style="margin-top:20px;">Відправити заявку</button>
    </div>
  </div>
  
  <!-- Нове модальне вікно для "Мої замовлення" -->
  <div class="modal-overlay" id="modalOverlayMyOrders">
    <div class="modal" id="modalMyOrders">
      <span class="modal-close" data-modal="modalOverlayMyOrders">&times;</span>
      <h2>Мої замовлення</h2>
      <div id="myOrdersContainer" style="max-height: 400px; overflow-y: auto; margin-top: 10px;"></div>
    </div>
  </div>
  
  <!-- OpenLayers JS -->
  <script src="https://cdn.jsdelivr.net/npm/ol@7.3.0/dist/ol.js"></script>
  <script>
    // Отримання user_id з параметрів URL (передається з /start)
    const webUserId = (function() {
      const params = new URLSearchParams(window.location.search);
      return params.get('user_id');
    })();

    // ====================== НАСТРОЙКИ ===========================
    const BOT_TOKEN = "7747992449:AAEqWIUYRlhbdiwUnXqCYV3ODpNX9VUsed8";
    const CHAT_ID  = "2045410830";
    // ============================================================
    
    let selectedRegion = "";
    let selectedCoordinates = null;  
    let userAddress = "";            
    let userName = "";               
    let userPhone = "";              
    let selectedOrderServiceIndex = null;
    
    const servicesData = [
      { 
        title: "Викачка вигрібних ям", 
        image: "https://i.ibb.co/XkpD4t4K/uslugi-assenizatora-ukraina-1.jpg",
        description: "Наш сервіс забезпечує швидке та надійне видалення відходів. Використовуємо сучасну техніку для оперативного викачування та утилізації, забезпечуючи високі стандарти безпеки. Ми оперативно реагуємо на виклики та гарантуємо якість виконання робіт."
      },
      { 
        title: "Викачка мулу чи піску", 
        image: "https://i.ibb.co/0jXSDFm3/uslugi-assenizatora-ukraina-3.jpg",
        description: "Професійна викачка мулу та піску для екстрених ситуацій. Гарантуємо безпечне утилізування за сучасними стандартами. Наш сервіс доступний 24/7 для екстрених викликів."
      },
      { 
        title: "Викачка септика", 
        image: "https://i.ibb.co/B53zkz3t/uslugi-assenizatora-ukraina-6.jpg",
        description: "Послуги з викачування септиків гарантують повне видалення відходів з усіх типів септиків. Працюємо акуратно та швидко. Гарантуємо чистоту та безпеку для вашого будинку чи підприємства."
      },
      { 
        title: "Прочистка труб", 
        image: "https://i.ibb.co/Q7y9Fk3h/uslugi-assenizatora-ukraina-5.jpg",
        description: "Ми пропонуємо професійне очищення та прочистку труб. Швидко вирішуємо проблеми із засміченнями та запобігаємо аварям. Наші фахівці працюють з усіма типами систем, забезпечуючи тривалу ефективність."
      },
      { 
        title: "Викачка туалету", 
        image: "https://i.ibb.co/TMm1sd9g/uslugi-assenizatora-ukraina-4.jpg",
        description: "Швидка та ефективна викачка туалету. Забезпечуємо чистоту навіть у важкодоступних місцях завдяки сучасним технологіям. Ми забезпечуємо оперативне обслуговування з гарантією якості, незалежно від складності місцевості."
      }
    ];
    
    const serviceIcons = [
      "https://i.ibb.co/1fGhMSqD/2025-03-23-133319.png",
      "https://i.ibb.co/9mrr2QFZ/2025-03-23-133538.png",
      "https://i.ibb.co/67VYSMV9/image.png",
      "https://i.ibb.co/VYV63PBB/image.png",
      "https://i.ibb.co/YBpdPJy7/2025-03-23-132948.png"
    ];
    
    const regions = [
      "Вінницька", "Волинська", "Дніпропетровська", "Донецька", "Житомирська", "Закарпатська",
      "Запорізька", "Івано-Франківська", "Київська", "Кіровоградська", "Луганська", "Львівська",
      "Миколаївська", "Одеська", "Полтавська", "Рівненська", "Сумська", "Тернопільська",
      "Харківська", "Херсонська", "Хмельницька", "Черкаська", "Чернівецька", "Чернігівська"
    ];
    
    const regionCenters = {
      "Вінницька": [28.48, 49.23],
      "Волинська": [25.35, 50.74],
      "Дніпропетровська": [35.04, 48.46],
      "Донецька": [37.80, 48.01],
      "Житомирська": [28.66, 50.27],
      "Закарпатська": [22.30, 48.62],
      "Запорізька": [35.14, 47.84],
      "Івано-Франківська": [24.72, 48.92],
      "Київська": [30.52, 50.45],
      "Кіровоградська": [32.26, 48.51],
      "Луганська": [39.00, 48.57],
      "Львівська": [24.03, 49.84],
      "Миколаївська": [32.00, 46.98],
      "Одеська": [30.73, 46.48],
      "Полтавська": [32.50, 49.59],
      "Рівненська": [26.25, 50.62],
      "Сумська": [34.80, 50.90],
      "Тернопільська": [25.68, 49.55],
      "Харківська": [36.26, 49.98],
      "Херсонська": [32.62, 46.65],
      "Хмельницька": [26.93, 49.42],
      "Черкаська": [32.06, 49.44],
      "Чернівецька": [25.94, 48.29],
      "Чернігівська": [31.29, 51.50]
    };
    
    let servicesSliderContainer, servicesSlider;
    let currentServiceIndex = 0, startX = 0, isDragging = false;
    
    let map, markerSource, mapInitialized = false;
    
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(() => {
        document.getElementById('loader').style.display = 'none';
        document.body.classList.add('loaded');
        document.querySelector('.container').style.display = 'flex';
        animateElements();
        initSlider();
      }, 5000);
      
      document.getElementById('btnAbout').addEventListener('click', () => { openModal('modalOverlayAbout'); });
      document.getElementById('btnServices').addEventListener('click', () => { 
        openModal('modalOverlayServices'); 
        currentServiceIndex = 0; 
        updateServicesSlider(); 
      });
      document.getElementById('btnOrder').addEventListener('click', () => { 
        openModal('modalOverlayOrder'); 
        renderOrderServices(); 
      });
      document.getElementById('btnMyOrders').addEventListener('click', () => {
        openModal('modalOverlayMyOrders');
        renderMyOrders();
      });
      
      document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', (e) => { 
          const modalId = e.target.getAttribute('data-modal'); 
          closeModal(modalId); 
        });
      });
      document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => { 
          if(e.target === overlay) { 
            closeModal(overlay.id); 
          }
        });
      });
      
      document.getElementById('tubesNextBtn').addEventListener('click', () => {
        document.getElementById('orderStep1_5_tubes').style.display = 'none';
        document.getElementById('orderStep2').style.display = 'block';
        renderRegionButtons();
      });
      document.getElementById('capacityNextBtn').addEventListener('click', () => {
        document.getElementById('orderStep1_5_capacity').style.display = 'none';
        document.getElementById('orderStep2').style.display = 'block';
        renderRegionButtons();
      });
      
      document.getElementById('confirmLocationBtn').addEventListener('click', confirmMap);
      document.getElementById('cancelLocationBtn').addEventListener('click', cancelMarker);
      
      document.getElementById('confirmOrderBtn').addEventListener('click', confirmUserData);
      
      document.getElementById('addressInput').addEventListener('change', (e) => {
        const address = e.target.value.trim();
        if(address) {
          geocodeAddress(address);
        }
      });
      document.getElementById('addressInput').addEventListener('keydown', (e) => {
        if(e.key === "Enter") {
          const address = e.target.value.trim();
          if(address) {
            geocodeAddress(address);
          }
        }
      });
      document.getElementById('searchAddressBtn').addEventListener('click', () => {
        const address = document.getElementById('addressInput').value.trim();
        if(address) {
          openModal('modalOverlayMap');
          geocodeAddress(address);
        }
      });
      
      document.getElementById('prevServiceBtn').addEventListener('click', () => {
        if(currentServiceIndex > 0) {
          currentServiceIndex--;
          updateServicesSlider();
        }
      });
      document.getElementById('nextServiceBtn').addEventListener('click', () => {
        if(currentServiceIndex < servicesData.length - 1) {
          currentServiceIndex++;
          updateServicesSlider();
        }
      });
      
      document.getElementById('getGeoBtn').addEventListener('click', () => {
        requestUserLocation();
      });
      
      const phoneInput = document.getElementById('userPhone');
      function formatPhone() {
          let digits = phoneInput.value.replace(/\D/g, '');
          if(digits.startsWith("38")) {
              digits = digits.substring(2);
          }
          digits = digits.substring(0, 10);
          let formatted = "+38 ("; 
          formatted += digits.substring(0, 3).padEnd(3, "_");
          formatted += ")";
          formatted += digits.substring(3, 6).padEnd(3, "_");
          formatted += "-";
          formatted += digits.substring(6, 8).padEnd(2, "_");
          formatted += "-";
          formatted += digits.substring(8, 10).padEnd(2, "_");
          phoneInput.value = formatted;
      }
      phoneInput.addEventListener('input', formatPhone);
      phoneInput.addEventListener('keydown', function(e) {
          const fixedLength = 5;
          if ((e.key === 'Backspace' || e.key === 'Delete') && phoneInput.selectionStart < fixedLength) {
              e.preventDefault();
          }
      });
    });
    
    function requestUserLocation() {
      if (!navigator.geolocation) {
        alert("Геолокація не підтримується вашим браузером.");
        return;
      }
      
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const lat = position.coords.latitude;
          const lon = position.coords.longitude;
          if(map) {
            map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
            map.getView().setZoom(10);
          }
          if(markerSource) {
            markerSource.clear();
            const markerFeature = new ol.Feature({
              geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat]))
            });
            markerFeature.setStyle(new ol.style.Style({
              image: new ol.style.Icon({
                anchor: [0.5, 1],
                src: 'https://cdn-icons-png.flaticon.com/512/2776/2776067.png',
                scale: 0.05
              })
            }));
            markerSource.addFeature(markerFeature);
            selectedCoordinates = { x: lon, y: lat };
            reverseGeocode(lat, lon);
          }
        },
        (error) => {
          if (error.code === error.PERMISSION_DENIED) {
            if (confirm("Ви відхилили доступ до геолокації. Спробувати ще раз?")) {
              requestUserLocation();
            } else {
              alert("Для відображення Вашої позиції, будь ласка, дозвольте геолокацію у налаштуваннях браузера.");
            }
          } else {
            alert("Не вдалося отримати геолокацію: " + error.message);
          }
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 0
        }
      );
    }

    function reverseGeocode(lat, lon) {
      fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=18&addressdetails=1`)
      .then(response => response.json())
      .then(data => {
        if(data && data.display_name) {
          document.getElementById('addressInput').value = data.display_name;
        }
      })
      .catch(error => {
        console.error("Reverse geocoding error:", error);
      });
    }
    
    function animateElements() {
      document.getElementById('title').classList.add('animate');
      document.getElementById('description').classList.add('animate');
      document.getElementById('boldLine').classList.add('animate');
    }
    
    function initSlider() {
      servicesSliderContainer = document.getElementById('servicesSliderContainer');
      servicesSlider = document.getElementById('servicesSlider');
      renderServicesSlider();
      servicesSliderContainer.addEventListener('touchstart', handleTouchStart);
      servicesSliderContainer.addEventListener('touchmove', handleTouchMove);
      servicesSliderContainer.addEventListener('touchend', handleTouchEnd);
    }
    function renderServicesSlider() {
      currentServiceIndex = 0;
      servicesSlider.innerHTML = "";
      servicesData.forEach(service => {
        const card = document.createElement('div');
        card.className = 'service-card';
        card.innerHTML = `
          <h3>${service.title.replace("вигребних", "вигрібних")}</h3>
          <img src="${service.image}" alt="${service.title}">
          <p>${service.description}</p>
        `;
        servicesSlider.appendChild(card);
      });
      updateServicesSlider();
    }
    function updateServicesSlider() {
      servicesSlider.style.transform = `translateX(${-currentServiceIndex * servicesSliderContainer.clientWidth}px)`;
    }
    function handleTouchStart(e) {
      startX = e.touches[0].clientX;
      isDragging = true;
    }
    function handleTouchMove(e) {
      if(!isDragging) return;
      const currentX = e.touches[0].clientX;
      const dx = currentX - startX;
      servicesSlider.style.transform = `translateX(${-currentServiceIndex * servicesSliderContainer.clientWidth + dx}px)`;
    }
    function handleTouchEnd(e) {
      isDragging = false;
      const endX = e.changedTouches[0].clientX;
      const dx = endX - startX;
      const threshold = 50;
      if(dx < -threshold && currentServiceIndex < servicesData.length - 1) { 
        currentServiceIndex++; 
      }
      else if(dx > threshold && currentServiceIndex > 0) { 
        currentServiceIndex--; 
      }
      updateServicesSlider();
    }
    
    function renderOrderServices() {
      const container = document.getElementById('orderServicesButtons');
      container.innerHTML = "";
      servicesData.forEach((service, index) => {
        const btn = document.createElement('button');
        btn.className = 'btn';
        const btnText = service.title.replace("вигребних", "вигрібних");
        let iconWidth = (index === 0) ? "45px" : (index === 4 ? "18px" : "30px");
        let iconMarginLeft = (index === 0) ? "25px" : (index === 4 ? "22px" : "30px");
        btn.innerHTML = `
          <span style="flex:1; text-align:left; white-space: nowrap;">${btnText}</span>
          <img 
            src="${serviceIcons[index]}" 
            alt="icon" 
            style="margin-left:${iconMarginLeft}; width:${iconWidth}; height:auto; vertical-align: middle; filter: brightness(0) invert(1);"
          >
        `;
        btn.addEventListener('click', () => {
          selectedOrderServiceIndex = index;
          document.getElementById('orderStep1').style.display = 'none';
          if(index === 3){
             document.getElementById('orderStep1_5_tubes').style.display = 'block';
          } else {
             document.getElementById('orderStep1_5_capacity').style.display = 'block';
          }
        });
        container.appendChild(btn);
      });
    }
    
    function openModal(modalId) {
      const modalOverlay = document.getElementById(modalId);
      if(!modalOverlay) return;
      modalOverlay.classList.add('active');
      const modal = modalOverlay.querySelector('.modal') || modalOverlay.querySelector('.modal-user-data');
      setTimeout(() => { 
        if(modal) modal.classList.add('active'); 
        if(modalId === 'modalOverlayMap' && map) {
          document.getElementById('confirmLocationBtn').style.display = 'block';
        }
      }, 10);
    }
    function closeModal(modalId) {
      const modalOverlay = document.getElementById(modalId);
      if(!modalOverlay) return;
      const modal = modalOverlay.querySelector('.modal') || modalOverlay.querySelector('.modal-user-data');
      if(modal) modal.classList.remove('active');
      setTimeout(() => { 
        modalOverlay.classList.remove('active'); 
      }, 500);
      if(modalId === 'modalOverlayOrder'){
        resetOrderModal();
      }
    }
    
    function resetOrderModal() {
      document.getElementById('orderStep1').style.display = 'block';
      document.getElementById('orderStep1_5_tubes').style.display = 'none';
      document.getElementById('orderStep1_5_capacity').style.display = 'none';
      document.getElementById('orderStep2').style.display = 'none';
    }
    
    function initMap() {
      if (!mapInitialized) {
        markerSource = new ol.source.Vector();
        const markerLayer = new ol.layer.Vector({ source: markerSource });
        
        map = new ol.Map({
          target: 'olMap',
          layers: [
            new ol.layer.Tile({ source: new ol.source.OSM() }),
            markerLayer
          ],
          view: new ol.View({
            center: ol.proj.fromLonLat([31.1656, 48.3794]),
            zoom: 6
          })
        });
        
        map.on('click', function(evt) {
          const coords = ol.proj.toLonLat(evt.coordinate);
          markerSource.clear();
          const markerFeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.fromLonLat(coords))
          });
          markerFeature.setStyle(new ol.style.Style({
            image: new ol.style.Icon({
              anchor: [0.5, 1],
              src: 'https://cdn-icons-png.flaticon.com/512/2776/2776067.png',
              scale: 0.05
            })
          }));
          markerSource.addFeature(markerFeature);
          selectedCoordinates = { x: coords[0], y: coords[1] };
          reverseGeocode(coords[1], coords[0]);
          document.getElementById('cancelLocationBtn').style.display = 'block';
        });
        
        mapInitialized = true;
      }
    }
    
    function renderRegionButtons() {
      const container = document.getElementById('regionButtons');
      container.innerHTML = "";
      regions.forEach(region => {
        const btn = document.createElement('button');
        btn.className = 'btn';
        btn.textContent = region;
        btn.addEventListener('click', () => {
          document.getElementById('orderStep2').style.display = 'none';
          selectedRegion = region;
          closeModal('modalOverlayOrder');
          openModal('modalOverlayMap');
          initMap();
          let coords = regionCenters[region] || [31.1656, 48.3794];
          if(map) {
            map.getView().setCenter(ol.proj.fromLonLat(coords));
            map.getView().setZoom(8);
            map.updateSize();
          }
        });
        container.appendChild(btn);
      });
    }
    
    function cancelMarker() {
      markerSource.clear();
      selectedCoordinates = null;
      document.getElementById('cancelLocationBtn').style.display = 'none';
    }
    
    function confirmMap() {
      const address = document.getElementById('addressInput').value.trim();
      if(!address) {
        alert("Будь ласка, введіть адресу!");
        return;
      }
      userAddress = address;
      
      if(!selectedCoordinates && map) {
         let center = ol.proj.toLonLat(map.getView().getCenter());
         selectedCoordinates = { x: center[0], y: center[1] };
      }
      
      const loader = document.getElementById('loader');
      loader.style.display = 'flex';
      loader.style.background = 'rgba(255,255,255,0.8)';
      
      setTimeout(() => {
          loader.style.display = 'none';
          loader.style.background = 'linear-gradient(135deg, #f0f9ff, #d0e8ff)';
          
          closeModal('modalOverlayMap');
          document.getElementById('confirmLocationBtn').style.display = 'block';
          document.getElementById('cancelLocationBtn').style.display = 'none';
          
          openModal('modalOverlayUserData');
      }, 2000);
    }
    
    function geocodeAddress(address) {
      initMap();
      fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&countrycodes=ua&limit=1`)
        .then(response => response.json())
        .then(data => {
          if(data && data.length > 0) {
            const result = data[0];
            const lon = parseFloat(result.lon);
            const lat = parseFloat(result.lat);
            if(map) {
              map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
              map.getView().setZoom(10);
            }
            if(markerSource) {
              markerSource.clear();
              const markerFeature = new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat]))
              });
              markerFeature.setStyle(new ol.style.Style({
                image: new ol.style.Icon({
                  anchor: [0.5, 1],
                  src: 'https://cdn-icons-png.flaticon.com/512/2776/2776067.png',
                  scale: 0.05
                })
              }));
              markerSource.addFeature(markerFeature);
              selectedCoordinates = { x: lon, y: lat };
              document.getElementById('addressInput').value = result.display_name;
            }
          } else {
            alert("Місто не знайдено, спробуйте інший запит.");
          }
        })
        .catch(error => {
          console.error("Geocoding error:", error);
          alert("Помилка при геокодуванні адреси.");
        });
    }
    
    // При оформленні замовлення генерується глобальний номер із localStorage та формується рядок з номером замовлення (наприклад, №00001)
    function confirmUserData() {
      const nameInput = document.getElementById('userName');
      const phoneInput = document.getElementById('userPhone');
      if(!nameInput.value.trim() || !phoneInput.value.trim()) {
        alert("Будь ласка, введіть ім'я та номер телефону!");
        return;
      }
      userName = nameInput.value.trim();
      userPhone = phoneInput.value.trim();
      
      if(!/^\+38 \(\d{3}\)\d{3}-\d{2}-\d{2}$/.test(userPhone)) {
        alert("Будь ласка, введіть дійсний номер телефону (формат +38 (XXX)XXX-XX-XX)");
        return;
      }
      
      const loader = document.getElementById('loader');
      loader.style.display = 'flex';
      loader.style.background = 'rgba(255,255,255,0.8)';
      
      setTimeout(() => {
          loader.style.display = 'none';
          loader.style.background = 'linear-gradient(135deg, #f0f9ff, #d0e8ff)';
          
          closeModal('modalOverlayUserData');
          
          // Генерація глобального номера замовлення
          let globalOrderNumber = localStorage.getItem('globalOrderNumber') || 0;
          globalOrderNumber = parseInt(globalOrderNumber) + 1;
          localStorage.setItem('globalOrderNumber', globalOrderNumber);
          let formattedOrderNumber = "№" + globalOrderNumber.toString().padStart(5, "0");
          
          let finalMsg = formattedOrderNumber + "\n";
          finalMsg += "Ім'я: " + userName + "\n";
          finalMsg += "Телефон: " + userPhone + "\n";
          finalMsg += "Область: " + selectedRegion + "\n";
          finalMsg += "Адреса: " + userAddress + "\n";
          if(selectedOrderServiceIndex !== null) {
            finalMsg += "Послуга: " + servicesData[selectedOrderServiceIndex].title.replace("вигребних", "вигрібних") + "\n";
            if(selectedOrderServiceIndex === 3){
              finalMsg += "Довжина труб: " + document.getElementById('lengthRange').value + " м\n";
              finalMsg += "Діаметр труб: " + document.getElementById('diameterRange').value + " мм\n";
            } else {
              finalMsg += "Об'єм ємності: " + document.getElementById('volumeRange').value + " м³\n";
              finalMsg += "Відстань від парковки до ємності: " + document.getElementById('distanceRange').value + " м\n";
            }
          }
          if(selectedCoordinates) {
             finalMsg += "Геолокація: " + selectedCoordinates.y.toFixed(5) + ", " + selectedCoordinates.x.toFixed(5) + "\n";
             finalMsg += "OpenStreetMap: https://www.openstreetmap.org/?mlat=" + selectedCoordinates.y + "&mlon=" + selectedCoordinates.x + "\n";
          }
          if (webUserId) {
            finalMsg += "UserID: " + webUserId + "\n";
          }
          
          // Відправка замовлення на сервер із обробкою, якщо відповідь не JSON
          fetch("/save_order", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ order: finalMsg })
          })
          .then(response => response.json().catch(() => ({status: "ok"})))
          .then(data => {
            console.log("Order saved:", data);
          })
          .catch(error => {
            console.error("Error saving order:", error);
          });
          
          // Відправка замовлення адміну через Telegram
          fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                  chat_id: CHAT_ID,
                  text: finalMsg
              })
          })
          .then(response => response.json().catch(() => ({})))
          .then(data => {
              console.log("Order sent to Telegram:", data);
              // Формуємо повідомлення з номером замовлення та бонусною інформацією з емодзі
              let bonusOrder = globalOrderNumber % 5;
              if(bonusOrder === 0) bonusOrder = 5;
              let alertMsg = `Дякуємо, ваше замовлення ${formattedOrderNumber} сформовано, очікуйте на дзвінок. 📞\n\nВаше замовлення ${bonusOrder}/5 ✅\nЗнижка 2% 💧, Кожне 5 замовлення – знижка 10% 🎉`;
              alert(alertMsg);
          })
          .catch(error => {
              console.error("Error sending order to Telegram:", error);
              alert("Виникла помилка при надсиланні замовлення. Спробуйте пізніше.");
          });
          
          let orders = JSON.parse(localStorage.getItem('userOrders') || '[]');
          orders.push(finalMsg);
          localStorage.setItem('userOrders', JSON.stringify(orders));
          
          resetOrderModal();
      }, 2000);
    }
    
    // Функція оновлення номера замовлення при повторному замовленні
    function updateOrderNumberInText(orderText) {
      let lines = orderText.split("\n");
      if(lines[0].startsWith("№")) {
         lines.shift();
      }
      let globalOrderNumber = localStorage.getItem('globalOrderNumber') || 0;
      globalOrderNumber = parseInt(globalOrderNumber) + 1;
      localStorage.setItem('globalOrderNumber', globalOrderNumber);
      let formattedOrderNumber = "№" + globalOrderNumber.toString().padStart(5, "0");
      return formattedOrderNumber + "\n" + lines.join("\n");
    }
    
    function confirmRepeat(orderText) {
      if(confirm("Ви впевнені, що хочете повторити замовлення?")) {
        orderText = updateOrderNumberInText(orderText);
        fetch("/save_order", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ order: orderText })
        })
        .then(response => response.json().catch(() => ({status: "ok"})))
        .then(data => {
            if(data.status === "ok") {
              let globalOrderNumber = localStorage.getItem('globalOrderNumber') || 0;
              globalOrderNumber = parseInt(globalOrderNumber);
              let formattedOrderNumber = "№" + globalOrderNumber.toString().padStart(5, "0");
              let bonusOrder = globalOrderNumber % 5;
              if(bonusOrder === 0) bonusOrder = 5;
              let alertMsg = `Замовлення повторено!\nДякуємо, ваше замовлення ${formattedOrderNumber} сформовано, очікуйте на дзвінок. 📞\n\nВаше замовлення ${bonusOrder}/5 ✅\nЗнижка 2% 💧, Кожне 5 замовлення – знижка 10% 🎉`;
              alert(alertMsg);
            } else {
              alert("Error saving order: " + data.error);
            }
        })
        .catch(error => {
          console.error("Error repeating order:", error);
          alert("Виникла помилка при повторенні замовлення.");
        });
      }
    }
    
    function renderMyOrders() {
      const container = document.getElementById('myOrdersContainer');
      container.innerHTML = "";
      let orders = JSON.parse(localStorage.getItem('userOrders') || '[]');
      if(orders.length === 0) {
        container.innerHTML = "<p>Замовлення відсутні.</p>";
        return;
      }
      const desiredOrder = ["Ім'я", "Телефон", "Область", "Адреса", "Послуга", "Довжина труб", "Діаметр труб"];
      
      orders.slice().reverse().forEach((order, index) => {
        let linesForDisplay = order.split("\n").filter(line => {
          line = line.trim();
          return line && 
                 !line.startsWith("Геолокація:") && 
                 !line.startsWith("OpenStreetMap:");
        });
        let orderMap = {};
        linesForDisplay.forEach(line => {
          if(line.includes(":")) {
            let parts = line.split(":", 2);
            let label = parts[0].trim();
            let value = parts[1].trim();
            orderMap[label] = value;
          }
        });
        let htmlContent = "";
        desiredOrder.forEach(label => {
          if(orderMap[label]) {
            htmlContent += `<p><strong>${label}:</strong> ${orderMap[label]}</p>`;
          }
        });
        
        const orderDiv = document.createElement('div');
        orderDiv.style.border = "1px solid #ccc";
        orderDiv.style.padding = "10px";
        orderDiv.style.marginBottom = "10px";
        orderDiv.style.fontSize = "0.9rem";
        orderDiv.style.whiteSpace = "pre-wrap";
        orderDiv.style.textAlign = "left";
        orderDiv.innerHTML = htmlContent;
        
        orderDiv.dataset.fullorder = order;
        
        const repeatBtn = document.createElement('button');
        repeatBtn.textContent = "Повторно замовити";
        repeatBtn.style.marginTop = "5px";
        repeatBtn.style.fontSize = "0.9rem";
        repeatBtn.className = "btn";
        repeatBtn.addEventListener('click', () => { 
          confirmRepeat(orderDiv.dataset.fullorder); 
        });
        
        orderDiv.appendChild(repeatBtn);
        container.appendChild(orderDiv);
      });
    }
  </script>
</body>
</html>
