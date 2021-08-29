// 2).
function ajaxSend(url, params) {
    // Отправляем запрос на сервер с помощью fetch (можно и с помощью Ajax jQuery)
    fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        // возвращаем JSON
        .then(json => render(json))
        // рендерим JSON
        .catch(error => console.error(error))
}

// Filter movies
// Закоментировать когда нужно сделать пагинацию ************************************
// 1). Ищем нашу форму с именем filter расположенную на sidebar
const forms = document.querySelector('form[name=filter]');

// при вызове метода submit у формы
forms.addEventListener('submit', function (e) {
    // Получаем данные из формы
    e.preventDefault();     // блокируем перезагрузку страницы
    let url = this.action;  // this указывает на нашу форму, action - фтрибут формы
    let params = new URLSearchParams(new FormData(this)).toString();
    // в переменную params передаем данные формы (параметры) - года, жанры
    ajaxSend(url, params);
    // ... и вызываем функцию ajaxSend в которую передаем url и param
});
// **********************************************************************************


function render(data) {
    // Рендер шаблона
    let template = Hogan.compile(html);
    let output = template.render(data);

    const div = document.querySelector('.left-ads-display>.row');
    div.innerHTML = output;
}

let html = '\
{{#movies}}\
    <div class="col-md-4">\
        <div class="movie-info editContent text-center mt-lg-4">\
            <div class="men-thumb-item">\
                <img src="/media/{{ poster }}" class="img-fluid" alt="">\
            </div>\
            <div class="movie-info-title">\
                <h4 class="movie_list">\
                    <a href="/{{ url }}" class="editContent">{{ title }}</a>\
                </h4>\
                \
                    \
                        \
                    \
                \
                <ul class="stars">\
                    <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star-o" aria-hidden="true"></span></a></li>\
                </ul>\
            </div>\
        </div>\
    </div>\
{{/movies}}'


// Add star rating
const rating = document.querySelector('form[name=rating]');

rating.addEventListener("change", function (e) {
    // Получаем данные из формы
    let data = new FormData(this);
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
        .then(response => alert("Рейтинг установлен"))
        .catch(error => alert("Ошибка"))
});

