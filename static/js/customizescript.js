
function item_popup(id) {
    $(".modal-content").html(null)
    $.ajax({
        url: '/item_details/',
        type: 'GET',
        data : {
                'product_id': id
        },
        success: function(resp){
            $(`<div class="modal-header">
                <h1 class="modal-title" id="myModalLabel">${ resp.data.name }</h1>
                <button type="button" class="btn-close btn-sm" data-bs-dismiss="modal" aria-hidden="true"></button>
            </div>
            <div class="modal-body">
                <div class="row justify-content-center bg-white align-items-center" style="min-height: 380px;">
                    <div class="col-md-5 p-0">
                        <div style="background: url('${ resp.data.image }') no-repeat center right; background-size: cover;  min-height: 380px;"></div>
                    </div>
                    <div class="col-md-7 bg-white p-4">
                        <div class="heading-block border-bottom-0 mb-3">
                            <h3 class="font-secondary nott ">${ resp.data.name }</h3>
                            <span>${ resp.data.price }</span>
                        </div>
                        <div class="widget-subscribe-form-result"></div>
                        <p>${ resp.data.description }</p>
                        <p id="id-cart" data-product ="${ resp.data.id }" data-action="add" class="btn btn-dark me-2 update-cart mt-4" onclick="update_from_poup()"><i class="icon-shopping-basket"></i></p>
                    </div>
                </div>
            </div>`).appendTo(".modal-content")
        }
      })
}
function update_from_poup(){
    let link = document.querySelector('#id-cart');
    if (link) {
        let productId = link.getAttribute('data-product');
        let action = link.getAttribute('data-action');
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
}