$(document).ready(function(){
  console.log('hhh')
  var cartdata=JSON.parse(localStorage.getItem('grandcart'))||[]  

  console.log(findtotal())

    $.ajaxSetup({
        headers: {
          "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
      })  

    if($('#loginstatus').val()=='true'){
      user_loggedin= true
     
    }
    else{
      user_loggedin= false
      $('viewcart').hide()
      

    }
    
    
    if(user_loggedin){
      console.log('hh')
      synccartdata(cartdata)
     
    }
    else{
      $('#totalamount').text(findtotal())
    }
  

      $('.cartbtn').each(function(){
        var product_id = $(this).data('productid')
        var item= cartdata.find(cartitems=>cartitems.product_id==product_id)
        if(item){
          $(this).hide()
          $(this).siblings('.viewcart').show()
        }
         
      })

      function addtocart(carts){
        cartdata.push(carts)
         localStorage.setItem('grandcart',JSON.stringify(cartdata))
      }  

      function removecart(index,cartitems){
        cartitems.splice(index,1)
        localStorage.setItem('grandcart',JSON.stringify(cartitems))
       
      }

      function findtotal(){
        sum = 0
        for(i=0;i<cartdata.length;i++){
          totprice=cartdata[i]
          sum+=parseFloat(totprice.price)*totprice.qty
        }
        return sum.toFixed(2)
      }



    $('.cartbtn').on('click',function(){
      var product_id = $(this).data('productid')
      var price = $(this).data('price')
      var product_name = $(this).data('product_name')
      var profile = $(this).data('profile')
      var container =$(this)
      var viewcart=container.siblings('.viewcart')
      console.log(viewcart)
      if(!user_loggedin){

       


        var item = {
            'product_id':product_id,
            'price':price,
            'qty':1,
            'product_name':product_name,
            'product_pic':profile
        }
        addtocart(item)
        viewcart.show()
        container.hide()


      }
      else{
        $.ajax({
            type: 'POST',
            url: $(this).data('url'),
            data: {
              'product': product_id
            },
            success: function (response) {
              data = response
              container.hide()
              console.log(data)
              
              viewcart.show()
              
            } 
        })
      }
       








        
    })

    function synccartdata(cartdata){
      
      if(cartdata.length>=1){
        $.ajax({
        type: 'POST',
        url: $('#hearder1').data('url'),
        data: {
        'cart': JSON.stringify(cartdata)
        },
        success: function (response) {
        data = response.status
        if(data){
          $('#totalamount').text(response.total)
          localStorage.removeItem('grandcart')
        }
       

      }
        })
      }
    }


    if ($('.table-shopping-cart').is(':visible') && !user_loggedin) {
      var table = $('.table-shopping-cart')
      var tbody = table.find('tbody')
      // console.log(tbody)
      if(cartdata){
        cartdata.forEach(cartitems => {
          var element =  ` <tr>
          <td>
              <figure class="itemside align-items-center">
                  <div class="aside"><img src="${cartitems.product_pic}" class="img-sm"></div>
                  <figcaption class="info">
                      <a href="#" class="title text-dark">${cartitems.product_name}</a>
                      <p class="text-muted small">Matrix: 25 Mpx <br> Brand: Canon</p>
                  </figcaption>
              </figure>
          </td>
          <td> 
                          <div class="col"> 
                              <div class="input-group input-spinner">
                                  <div class="input-group-prepend">
                                  <button class="btn btn-light minus" type="button" id="button-plus"> <i class="fa fa-minus"></i> </button>
                                  </div>
                                  <input type="text" class="form-control" data-product_id="${cartitems.product_id}"  value="${cartitems.qty}">
                                  <div class="input-group-append">
                                  <button class="btn btn-light plus" type="button" id="button-minus"> <i class="fa fa-plus"></i> </button>
                                  </div>
                              </div> <!-- input-group.// -->
                          </div> 
          </td>
          
          <td> 
              <div class="price-wrap"> 
                  <var class="price">$ ${cartitems.price*cartitems.qty}</var> 
                  <small class="text-muted">$ ${cartitems.price} </small> 
              </div> <!-- price-wrap .// -->
          </td>
          <td class="text-right"> 
          
          </td>`
          
          tbody.append(element)
          
        });
        $('#totalprice').text('$'+findtotal())
      }
  }

  $('.plus').on('click',function(){
    // console.log('item')

    var input = $(this).parent().siblings('input')
    var product_id=input.data('product_id')

    var productprice = input.data('Price')
  
    var container = $(this).closest('tr')
    var price_div = container.find('td').eq(2)
    console.log(productprice)
    if(user_loggedin){
      console.log(product_id)

      $.ajax({
        type: 'POST',
        url: $(this).data('url'),
        data: {
          'product': product_id
        },
        success: function (response) {
          data = response
          var count = data.quandity
          input.val(count)
          console.log(data)
          price_div.find('.price').text('$'+data.subtotal)
          $('#totalprice').text('$'+data.toatal)
          
        } 
    })


    }
    else{

      var item = cartdata.find(cartitems=>cartitems.product_id==product_id)
    if(item ){
      item.qty+=1
      var count = item.qty
      var subtotal = item.qty*item.price
      console.log(price_div.find('.price'))
      price_div.find('.price').text('$'+subtotal)
      localStorage.setItem('grandcart',JSON.stringify(cartdata))
      input.val(count)
      $('#totalprice').text('$'+findtotal())
    }

    }
    
  })

  $('.minus').on('click',function(){
    // console.log('item')

    var input = $(this).parent().siblings('input')
    var product_id=input.data('product_id')
    var container = $(this).closest('tr')
    var price_div = container.find('td').eq(2)

    // console.log('item')

    if(user_loggedin){
      console.log(product_id)

      $.ajax({
        type: 'GET',
        url: $(this).data('url'),
        data: {
          'product': product_id
        },
        success: function (response) {
          data = response
          var count = input.val()-1
         if (count>0){

          input.val(count)
          console.log(data)
          price_div.find('.price').text('$'+data.subtotal)
          $('#totalprice').text('$'+data.toatal)
          

         }
         else{
          container.remove()

         }

         $('#totalprice').text('$'+data.toatal)
         
         
          
        } 
    })


    }
    else{
      var item = cartdata.find(cartitems=>cartitems.product_id==product_id)
      if(item){
        item.qty-=1
        var count = item.qty
        if(count>0){
  
        localStorage.setItem('grandcart',JSON.stringify(cartdata))
        var subtotal = item.qty*item.price
        console.log(price_div.find('.price'))
        price_div.find('.price').text('$'+subtotal)
        console.log(price_div)
        input.val(count)
        $('#totalprice').text('$'+findtotal())
  
        }
        else{
          var index = cartdata.indexOf(item)
          removecart(index,cartdata)
          container.remove()
  
  
        }
        
      }
    }

   
  })
  $('#emailcheck').on('change',function(){

    $.ajax({
      type: 'POST',
      url: $('#emailcheck').data('url'),
      data: {
        'email': $('#email').val()
      },
      success: function (response) {
        data = response.exist
        if(data){
          $('#password').show()
          // $('#regform').attr('action','/signup')


        }
        else{
          $('#sendotp').show()
          $('#password').show()

          $('#loginbtn').hide()
          // $('#regform').attr('action','/signup')

        }

      }
    })

  })
  
  $('#stars .fa-star').on('click',function(){
    var index = $(this).index()
    $('#stars .fa-star').each(function(i){
      console.log(index)
      if(i<index){
        $(this).removeClass('checked')
        $(this).addClass('checked')
      }
      else{
        $(this).removeClass('checked')
      }
    })
    $('#rating').val(index)
  })


 
})

