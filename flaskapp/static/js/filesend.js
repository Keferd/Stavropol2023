let sendfilebtn = document.querySelector(".aside__button_submit");

sendfilebtn.addEventListener("click", function (e) {
    e.preventDefault();
    

    let input = document.getElementById("file");
    let camera = document.getElementById("camera").value
    let file = input.files[0];
    
    let formdata = new FormData();
    formdata.append('file', file);
    formdata.append('camera', JSON.stringify(camera));
    formdata.append('test', 'test is work');


    if (typeof file != 'undefined') {
        document.getElementById("download").innerHTML = `
            <div class="img__container">
                <img class="img__loading" src="static/img/loading.png" alt="loading">
            </div>

            <style>
                .img__container {
                    flex: 1;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }

                .img__loading {
                    width: 100px;
                    height: 100px;
                    animation: rotate_img 0.5s linear infinite;
                }

                @keyframes rotate_img {
                    0% {
                      transform: rotate(0deg);
                    }
                    100% {
                      transform: rotate(360deg);
                    }
                  }
            </style>
        `;
        

        fetch("/api/file",
        {
            method: "POST",
            body: formdata,
            /*headers: {
                'Content-Type': 'multipart/form-data'
            }*/
        })
        .then( response => {
            response.json().then(function(data) {
                console.log(data);
                console.log(data.image_url);
                console.log(data.json_object);

                var encodedImage = data.image_url;

                // Декодирование Base64 в бинарные данные
                var decodedImage = atob(encodedImage);

                // Преобразование бинарных данных в массив байт
                var byteCharacters = decodedImage.split('').map(char => char.charCodeAt(0));
                var byteArray = new Uint8Array(byteCharacters);

                // Тип изображения (зависит от формата изображения)
                var imageType = 'image/jpeg';

                // Создание объекта Blob из массива байт с правильным типом
                var blob = new Blob([byteArray], { type: imageType });

                // Создание объекта URL для использования в src атрибуте изображения
                var imageUrl = URL.createObjectURL(blob);


                document.getElementById("download").innerHTML = `
                    <a href="" class="return_button">
                        Вернуться
                    </a>
                    <h2 class="main__h2">
                        Результат
                    </h2>
                    <div class="result__img"> 
                        <img src=` + imageUrl + ` alt="Изображение">
                    </div>

                    <a class="aside__button_a" href=` + imageUrl + ` download="result.jpg">
                        <input  class="aside__button_download" type="button" value="Скачать">
                    </a>

                    <div style="font-size: 32px;">
                        ` + data.json_object + `
                    </div>
                `;
            });
        })
        .catch( error => {
            alert(error);
            console.error('error:', error);
        });
        
    }
    else {
        document.getElementById("error").innerHTML = `
            <div style="color: red;">
                Выберите файл
            </div>
        `
    }
});