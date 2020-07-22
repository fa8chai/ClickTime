document.addEventListener('DOMContentLoaded',()=>{
    if(document.querySelector('.b-btn').classList.contains('unblock')){
        document.querySelector('.fo').style.display='none';
    }
    if(document.querySelector('.fo').classList.contains('unfollow')){
        document.querySelector('.b-btn').style.display='none';
    }
    document.querySelector('.b-btn').onclick = ()=>{
        if(document.querySelector('.b-btn').classList.contains('block')){
            document.querySelector('.b-btn').disabled = true;
            var username = document.querySelector('.username').textContent;
            var xhttp = new XMLHttpRequest();
            var url =`/ajax/8/block/?username=${username}`;
            xhttp.open('GET', url);
                
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var data = JSON.parse(this.response); 
                    document.querySelector('.b-btn').classList.remove('block');
                    document.querySelector('.b-btn').classList.add('unblock');
                    document.querySelector('.b-btn').disabled = false;
                    document.querySelector('.b-btn').innerHTML = 'Unblock';
                    document.querySelector('.fo').style.display='none';

                }
                };
               
            xhttp.send();
        }
        else{
            document.querySelector('.b-btn').disabled = true;
            var username = document.querySelector('.username').textContent;
            var xhttp = new XMLHttpRequest();
            var url =`/ajax/9/unblock/?username=${username}`;
            xhttp.open('GET', url);
        
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                var data = JSON.parse(this.response); 
                document.querySelector('.b-btn').classList.remove('unblock');
                document.querySelector('.b-btn').classList.add('block');
                document.querySelector('.b-btn').disabled = false;
                document.querySelector('.b-btn').innerHTML = 'Block';
                document.querySelector('.fo').style.display = 'inline';            
            }
            };
       
        xhttp.send();
        }
    }
    document.querySelector('.fo').onclick = ()=>{
        if(document.querySelector('.fo').classList.contains('follow')){
            document.querySelector('.b-btn').style.display='inline';

            document.querySelector('.fo').disabled = true;
            var username = document.querySelector('.username').textContent;
            var xhttp = new XMLHttpRequest();
            var url =`/ajax/3/follow/?username=${username}`;
            xhttp.open('GET', url);
                
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var data = JSON.parse(this.response); 
                    document.querySelector('.fo').classList.remove('follow');
                    document.querySelector('.fo').classList.add('unfollow');
                    document.querySelector('.fo').disabled = false;
                    document.querySelector('.fo').innerHTML = 'Unfollow';
                    document.querySelector('.b-btn').style.display='none';

                }
                };
               
            xhttp.send();
        }
        else{
            document.querySelector('.fo').disabled = true;
            var username = document.querySelector('.username').textContent;
            var xhttp = new XMLHttpRequest();
            var url =`/ajax/4/unfollow/?username=${username}`;
            xhttp.open('GET', url);
        
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                var data = JSON.parse(this.response); 
                document.querySelector('.fo').classList.remove('unfollow');
                document.querySelector('.fo').classList.add('follow');
                document.querySelector('.fo').disabled = false;
                document.querySelector('.fo').innerHTML = 'Follow';   
                document.querySelector('.b-btn').style.display='inline';
         
            }
            };
       
        xhttp.send();
        }
    }
    

    
})