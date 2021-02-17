var updateBtns = document.getElementsByClassName('update-cart')
for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){

        var productId = this.dataset.product
        var action = this.dataset.action
        console.log ('USER:',user)

        if (user === 'AnonymousUser'){
            alert('Customer must log in First !');

            console.log('No user logged in')
        }else{
            updateUserOrder(productId,action)
        }
       })

    }

function updateUserOrder(productId,action){

     console.log('Logged In. Sending Data ..... ')

     var url = '/updateitem/'
     fetch (url, {
        method: 'POST',
        headers : {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body :JSON.stringify({'productId':productId,'action':action})

     })
     .then((response) => {
        return response.json()
     })
     .then((data) => {
        console.log ('data:',data)
        location.reload()


     })
}