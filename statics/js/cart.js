
var updateButtons = document.getElementsByClassName('update-cart')
for(var i = 0; i < updateButtons.length; i++){
    updateButtons[i].addEventListener('click',function(){
        var itemId = this.dataset.item;
        var action = this.dataset.action;
        console.log(itemId)
        console.log(action)
        if(user==='AnonymousUser'){
            console.log('not logged in');
        }else{
            updateUserOrder(itemId,action)
        }
    })
}


function updateUserOrder(itemId,action){
    fetch('/update_item/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'itemId': itemId, 'action': action}),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', data);
        
    })
    .catch(error => {
        console.error('Error:', error);
    });
    location.reload();
}

