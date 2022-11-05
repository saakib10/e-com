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
        location.reload()
     })
}

$.ajax({
    url : '{% url "user" %}',
    type : "POST",

    success: function(response) {
        console.log(response.items)
    }
});

// pop up form 

// Code By Webdevtrick ( https://webdevtrick.com )
(function(){
    $('html').addClass('js');
    
    var contactForm = {
      container: $('#contact'),
      config: {
        effect: 'slideToggle',
        speed: 200
      },
      
      init: function(config){
        $.extend(this.config, config);
        
        $('#c-btn').on('click', this.show);
      },
  
      show: function(){
        var cf = contactForm,
            container = cf.container,
            config = cf.config;
                      
  
        if(container.is(':hidden')){
          cf.close.call(container);
          container[config.effect]
          (config.speed);
        }
      },
  
      close: function(){
        var $this = $('#contact'); 
        
        if($this.find('span.close').length) return;
  
        $('<span class=close>-</span>')
          .prependTo(this)
          .on('click', function(){
          $this[contactForm.config.effect](contactForm.config.speed);
        })
      }
    };
  
  contactForm.init({
    effect: 'fadeToggle',
    speed: 200
  });
  })();