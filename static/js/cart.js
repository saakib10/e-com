var updateBtns = document.getElementsByClassName('update-cart')
for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){

        var productId = this.dataset.product
        var action = this.dataset.action

        if (user === 'AnonymousUser'){
            alert('Customer must log in First !');
        }else{
            updateUserOrder(productId,action)
        }
       })
    }

function updateUserOrder(productId,action){
      $(".cart-item-number").html(null)
      $.ajax({
            url: '/updateitem/',
            type: 'GET',
            data : {
                    'productId': parseInt(productId),
                    'action':action
            },
            success: function(resp){
                $(`<span class="top-cart-number">${resp.data}</span>`).appendTo(".cart-item-number")
                }
          });
     
}
$(".btttn").on('click',function() {
  $("#cart-total").html(null)
  var productId = this.dataset.product
  var action = this.dataset.action
  $.ajax({
        url: '/updateitem/',
        type: 'GET',
        data : {
                'productId': parseInt(productId),
                'action':action
        },
        success: function(resp){
            location.reload()
            }
      });
});