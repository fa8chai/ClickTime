document.addEventListener('DOMContentLoaded',()=>{
    function fol(){
        var xhttp = new XMLHttpRequest();
        var url ='/ajax/7/fol/';
        xhttp.open('GET', url);
        
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.response); 
            document.querySelector('.followers').innerHTML = data.followers;
            document.querySelector('.following').innerHTML = data.following;
            }
        };
        xhttp.send();
    }


    setInterval(fol(), 5000);
    
})