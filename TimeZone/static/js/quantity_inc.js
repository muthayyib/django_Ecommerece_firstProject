$(document).ready(function(){
    $('.increment-btn').click(function(e){
        e.preventDefault();

        var inc_valaue = $(this).closest('.product-data').find('.qt-input').val();
        var value = parseInt(inc_valaue,10);
        value = isNaN(value)? 0 : value; 
        if (value < 10){
            value++;
            $(this).closest('.product-data').find('.qt-input').val(value);
        }
    });
    $('.decrement-btn').click(function(e){
        e.preventDefault();

        var dec_valaue = $(this).closest('.product-data').find('.qt-input').val();
        var value = parseInt(dec_valaue,10);
        value = isNaN(value)? 0 : value; 
        if (value > 1){
            value--;
            $(this).closest('.product-data').find('.qt-input').val(value);
        }
    });
});