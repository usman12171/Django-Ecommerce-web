
$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml=document.getElementById('table-row');
    $.ajax({
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log(id)
            eml.remove()   
            document.getElementById('total').innerText=data.total
            document.getElementById('total_amount').innerText=data.total_amount      
        }
    });
});
$('.plus-cart').click(function(e){
    e.preventDefault();
    var id = $(this).attr("pid").toString();
    var eml =this.parentNode.children[1]
    console.log(id)
    $.ajax({
        url:"/pluscart",
        type:"GET",
        async: false,
        data:{
            prod_id:id
        },
        success:function(data){
            console.log(data)
            eml.innerText = data.quantity
            document.getElementById('total').innerText=data.total
            document.getElementById('total_amount').innerText=data.total_amount 
        }
    });
});
$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml =this.parentNode.children[1]
    console.log(id)
    $.ajax({
        url:"/minuscart",
        async: false,
        data:{
            prod_id:id
        },
        success:function(data){
            console.log(data)
            eml.innerText = data.quantity 
            document.getElementById('total').innerText=data.total
            document.getElementById('total_amount').innerText=data.total_amount 
        }
    });
});
$('.add-cart').click(function(e){
    e.preventDefault();
    var id = $(this).attr("pid").toString();
    console.log(id)
    $.ajax({
        url:"/addcart",
        type:"GET",
        async: false,
        data:{
            p_id:id
        },
        success:function(data){
            if(data.message == 'true')
                alert(data.message);
            else
                alert(data.messageerror);  
        }
    });
});

var email=document.querySelector("#emailfield");
var feedback=document.querySelector(".invalid_feedback");
  email.addEventListener("keyup",function(e){
    console.log('3333',4444)
    var valu=e.target.value;
    email.classList.remove('invalid');
    feedback.style.display = "none";
    console.log(valu);
    $.ajax({
        url:"/emailvalid",
        type:"GET",
        async: false,
        data:{
            values:valu
        },
             success:function(data){
                console.log(data.email)
                email.classList.add('invalid');
                feedback.style.display = "block";
                feedback.innerHTML = `<p>${data.email}</p>`
             }
    });
  });
   

    
