document.addEventListener('DOMContentLoaded',()=>{
    document.querySelector('.btn-submit').hidden = true;
    document.querySelector('.btn-edit').hidden = true;
    var images_input = document.querySelector('#id_image');
    images_input.onchange = ()=>{
        document.querySelector('.btn-edit').hidden = false;
        Object.keys(images_input.files).forEach(key => {

            var image = document.createElement('img');
            image.classList.add('image1');
            document.querySelector('.image-container').append(image);
            image.src = window.URL.createObjectURL(images_input.files[key])
            
        });
        document.querySelector('.btn-edit').onclick = () =>{
            location.reload();
        }
        

    
        document.querySelector('.btn-submit').hidden = false;
        document.querySelector('.form-control').style.display = "block";
       
    }
})