document.addEventListener('DOMContentLoaded',()=>{

    var objDiv = document.getElementById("scroll");
    objDiv.scrollTop = objDiv.scrollHeight - objDiv.clientHeight;;

    document.querySelector('.post-active').classList.add('carousel-item','active');
    
    var username = document.querySelector('#username').value;
    var post_id = document.querySelector('.post_id').textContent;

    function ch_like(){
    var xhttp = new XMLHttpRequest();
    var url =`/ajax/6/ch_like/?post_id=${post_id}`;
    xhttp.open('GET', url);
        
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        var data = JSON.parse(this.response); 
        document.querySelector('.like_btn').innerHTML = data.data;
        document.querySelector('.like_btn').disabled = false;
        }
    };
    xhttp.send();
    }
    ch_like()


    ws = new WebSocket(
        'ws://'+ window.location.host+ '/ws/'+post_id+'/' 
    );

    
    
    ws.onopen = e => {      
        console.log("Connected");      
    }

    ws.onclose = e => {
        console.error('Socket closed unexpectedly');
    };

    ws.onerror = function (e) {  
        console.error(e);  
    }

    ws.onmessage = e => {
        var data = JSON.parse(e.data);
        if ( data.message == 'like' ){
            var xhttp = new XMLHttpRequest();
            var url =`/ajax/5/like/?post_id=${post_id}`;
            xhttp.open('GET', url);
        
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                var data = JSON.parse(this.response); 
                console.log(data);
            }
            };
            xhttp.send();
            document.querySelector('.likes').innerHTML = data.likes ;
            ch_like();
        }
        else if (data.message == 'liked'){
            ch_like();
        }
        else if( data.message == 'dislike' ){
            document.querySelector('.likes').innerHTML = data.likes ;
            ch_like();
        }
        else if ( data.message == 'comment' ){
            var xhttp = new XMLHttpRequest();
            var url =`/ajax/10/comment/?post_id=${post_id}`;
            xhttp.open('GET', url);
        
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                var data = JSON.parse(this.response); 
                console.log(data);
            }
            };
            xhttp.send();
            var smallDiv = document.createElement('small');
            var div = document.createElement('div');
            div.classList.add('comment');
            var a = document.createElement('a');
            a.href = window.location.host + '/u/' + data.user + '/' ;
            var hp = document.createElement('small');
            var sm = document.createElement('div');
            sm.classList.add('mt-auto','mb-auto');
            var img = document.createElement('img');
            img.classList.add('post-img');
            img.src = data.img;
            a.classList.add('row')
            a.append(img);
            sm.append(hp);
            a.append(sm);
            var p = document.createElement('p');
            var small = document.createElement('small');
            p.innerHTML = data.text;
            small.innerHTML = data.created_on;
            hp.innerHTML = data.user;
            smallDiv.append(div);
            div.append(a);
            div.append(p);
            div.append(small);
            
            var comments_div = document.querySelector('.comments');
            
            const isScrolledToBottom = comments_div.scrollHeight - comments_div.clientHeight <= comments_div.scrollTop + 1;
            comments_div.append(smallDiv);    

            // scroll to bottom if isScrolledToBottom is true
            if (isScrolledToBottom) {
                comments_div.scrollTop = comments_div.scrollHeight - comments_div.clientHeight
            }

        }
        else{
            console.log('Unexpected WebSocket message')
        }
        
    }

    document.querySelector('.like_btn').onclick = () => {
        if (document.querySelector('.like_btn').innerHTML == 'Liked'){
            ws.send(JSON.stringify({
                'message': 'dislike',
                'post_id':post_id,
                'username':username
            }))
            document.querySelector('.like_btn').disabled = true;
        }

        else if (document.querySelector('.like_btn').innerHTML == 'Like') {
            ws.send(JSON.stringify({
                'message': 'like',
                'post_id':post_id,
                'username':username
            }))
            document.querySelector('.like_btn').disabled = true;
        }
        else{
            console.log('Unexpected error')
        }
    }
    

    document.querySelector('.submit').onclick = () => {
        var comment = document.getElementById('comment').value;
        ws.send(JSON.stringify({
            'message':'comment',
            'comment':comment,
            'post_id':post_id,
            'username':username
        }))
        document.getElementById('comment').value = '';
    }

    

})
