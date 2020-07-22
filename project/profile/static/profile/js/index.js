document.addEventListener('DOMContentLoaded',()=>{
    console.log('hi');
    var username = document.getElementById('id_username');
    co = username.value.slice(0);
    var error = document.getElementById('username');
        

    username.addEventListener('change', ()=>  {

    if (username.value.length == 0){
        username.value = co;
        document.querySelector('.submit').disabled = false;
        username.style.border = '';
        error.innerHTML = '';
    }
    else if (username.value == co){
        error.innerHTML = '';
        username.style.border = '';
        document.querySelector('.submit').disabled = false;
        return false;
    }
    else if (username.value.length <= 3){
        error.innerHTML = 'Username is too short!';
        document.querySelector('.submit').disabled = true;
        username.style.border = 'solid red 2px';
    }
    else if (username.value.includes('@')){
        error.innerHTML = "Username can't contain '@'";
        username.style.border = 'solid 2px red';
        document.querySelector('.submit').disabled = true;
    }
    else{
    var xhttp = new XMLHttpRequest();
    var url =`ajax/1/validate_username/?username=${username.value}`;
        
    xhttp.open('GET', url);
        
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.response);
            if (data.taken){
                error.innerHTML = `<span class='username_taken'>${username.value}</span> is already taken`;
                username.style.border = 'solid 2px red';
                document.querySelector('.submit').disabled = true;
            }
            else{
                document.querySelector('.submit').disabled = false;
                username.style.border = 'solid 2px green';
                error.innerHTML = '';

            }
        }
        else{
            console.log('ERROR');
        }
        };
       
    xhttp.send();
    }
})



})