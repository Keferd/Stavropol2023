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
                    <h2 class="main__h2">
                        Результат
                    </h2>
                    <div id="resizable-container"  class="result__img"> 
                        <img id="resizable-image" src=` + imageUrl + ` alt="Изображение">
                    </div>

                    <a class="aside__button_a" href=` + imageUrl + ` download="result.jpg">
                        <input  class="aside__button_download" type="button" value="Скачать">
                    </a>

                    <div style="font-size: 32px;">
                        ` + data.json_object + `
                    </div>
                `;

                let isResizing = false;
                let container = document.getElementById('resizable-container');
                let image = document.getElementById('resizable-image');

                container.addEventListener('mousedown', (event) => {
                isResizing = true;
                document.addEventListener('mousemove', handleMouseMove);
                document.addEventListener('mouseup', () => {
                    isResizing = false;
                    document.removeEventListener('mousemove', handleMouseMove);
                });
                });

                function handleMouseMove(event) {
                if (isResizing) {
                    let newWidth = event.clientX - container.getBoundingClientRect().left;
                    container.style.width = `${newWidth}px`;
                }
                }
            });
        })
        .catch( error => {
            alert(error);
            console.error('error:', error);
        });
        
    }
    else {
        document.getElementById("download").innerHTML = `
            <div style="color: red; margin-left: 10px">
                Выберите файл
            </div>
        `
    }
});