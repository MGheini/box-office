// This event is triggered when the star rating is modified or changed
// This event also allows you to access these parameters
// value: the selected rating value
// caption: the caption for the selected rating
$('#inputRate').on('rating.change', function(event, value, caption) {
    console.log(value);
    console.log(caption);
    // we'll use this for saving rate and ...
});


// use this to convert all numbers to persian
// $(document).ready(function() {
//     persian={0:'۰',1:'۱',2:'۲',3:'۳',4:'۴',5:'۵',6:'۶',7:'۷',8:'۸',9:'۹'};
//     function traverse(el){
//         if(el.nodeType==3){
//             var list=el.data.match(/[0-9]/g);
//             if(list!=null && list.length!=0){
//                 for(var i=0;i<list.length;i++)
//                     el.data=el.data.replace(list[i],persian[list[i]]);
//             }
//         }
//         for(var i=0;i<el.childNodes.length;i++){
//             traverse(el.childNodes[i]);
//         }
//     }
//     traverse(document.body);
// });

    
    // start proto - global vars
    var ticketType =0;
    var ticketPrice=0;
    var ticketNum=0;
    // start proto

// functionality is only for prototype, we'll erase it later.
$(document).ready(function() {
    var navListItems = $('ul.setup-panel li a'),
        allWells = $('.setup-content');

    allWells.hide();

    navListItems.click(function(e)
    {
        e.preventDefault();
        var $target = $($(this).attr('href')),
            $item = $(this).closest('li');
        
        if (!$item.hasClass('disabled')) {
            navListItems.closest('li').removeClass('active');
            $item.addClass('active');
            allWells.hide();
            $target.show();
        }
    });
    
    $('ul.setup-panel li.active a').trigger('click');
    
    $('.edit-step-1').on('click', function(e) {
        e.preventDefault();
        $('ul.setup-panel li:eq(0)').removeClass('disabled');
        $('ul.setup-panel li:eq(1)').addClass('disabled');
        $('ul.setup-panel li:eq(2)').addClass('disabled');
        $('ul.setup-panel li a[href="#step-1"]').trigger('click');
    });


    $('#activate-step-2').on('click', function(e) {
        // we must use xhr here.
        e.preventDefault();
        var flag = false;

        // start proto
        if(document.getElementById('radio1').checked) {
            $('ul.setup-panel li:eq(0)').addClass('disabled');
            $('ul.setup-panel li:eq(1)').removeClass('disabled');
            $('ul.setup-panel li a[href="#step-2"]').trigger('click');
            ticketType = document.getElementById('type1').innerHTML;
            ticketPrice = document.getElementById('price1').innerHTML;
            ticketNum = document.getElementById('num1').value;
            flag = true;
        }
        else if (document.getElementById('radio2').checked) {
            $('ul.setup-panel li:eq(0)').addClass('disabled');
            $('ul.setup-panel li:eq(1)').removeClass('disabled');
            $('ul.setup-panel li a[href="#step-2"]').trigger('click');
            ticketType = document.getElementById('type2').innerHTML;
            ticketPrice = document.getElementById('price2').innerHTML;
            ticketNum = document.getElementById('num2').value;
            flag = true;
        }
        else if (document.getElementById('radio3').checked) {
            $('ul.setup-panel li:eq(0)').addClass('disabled');
            $('ul.setup-panel li:eq(1)').removeClass('disabled');
            $('ul.setup-panel li a[href="#step-2"]').trigger('click');
            ticketType = document.getElementById('type3').innerHTML;
            ticketPrice = document.getElementById('price3').innerHTML;
            ticketNum = document.getElementById('num3').value;
            flag = true;
        }
        else { // none is chosen
            var error = document.getElementById('error-msg1');
            error.style.visibility = 'visible';
            setTimeout(function() {
                error.style.visibility = 'hidden';
            }, 3000);
        }
        if(flag) {
            document.getElementById('factorBody').innerHTML = "";
            var newTr;
            for(var i = 0; i < parseInt(ticketNum); i++) {
                newTr = document.createElement('tr');
                newTr.innerHTML += '<td>'+ticketType+'</td>'
                    +'<td>برج میلاد</td>'
                    +'<td>۲۱ آبان ۹۴</td>'
                    +'<td>۱۸:۳۰</td>'
                    +'<td>'+ (i+12) +'</td>'
                    +'<td>'+ticketPrice+'</td>';
                document.getElementById('factorBody').appendChild(newTr);
            }

            newTr = document.createElement('tr');
            var tp = (parseInt(ticketNum)*parseInt(ticketPrice));
            newTr.innerHTML = '<tr><td colspan="20" style="text-align: left">مبلغ کل : <span id="totalPrice">'+ tp +'</span> تومان</td></tr>'
            document.getElementById('factorBody').appendChild(newTr);
        }
        // end proto

        // this part must be commented for prototype, but it is actually main part!!!
        // $('ul.setup-panel li:eq(0)').addClass('disabled');
        // $('ul.setup-panel li:eq(1)').removeClass('disabled');
        // $('ul.setup-panel li a[href="#step-2"]').trigger('click');
    });

    $('#activate-step-3').on('click', function(e) {
        e.preventDefault();
        $('ul.setup-panel li:eq(0)').addClass('disabled');
        $('ul.setup-panel li:eq(1)').addClass('disabled');
        $('ul.setup-panel li:eq(2)').removeClass('disabled');
        $('ul.setup-panel li a[href="#step-3"]').trigger('click');
        
        // start proto
        var tp = (parseInt(ticketNum)*parseInt(ticketPrice));
        document.getElementById('acceptedTotalPrice').innerHTML = tp;
        // end proto
    });
});

$("td").click(function () {
   $(this).find('input:radio').attr('checked', true);
});

// start proto
document.getElementById('approvePay').addEventListener('click', function(e) {
    e.preventDefault();
    var inputCardNum = document.getElementById('inputCardNum').value;
    if(inputCardNum === "1111-1111-1111-1111") {
        window.location.href = "view-receipt.html";
    }

    else {
                    var error = document.getElementById('error-msg2');
            error.style.visibility = 'visible';
            setTimeout(function() {
                error.style.visibility = 'hidden';
            }, 3000);
    }
});
// end proto