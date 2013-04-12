$(function(){
    $('#uploadAvatarBtnLayout button').addClass('button-deep-color');
    
    $('#uploadAvatarInputFile').mouseover(function(){
        $('#uploadAvatarBtnLayout button').removeClass('button-deep-color').addClass('button-light-color');
    }).mouseout(function(){
        $('#uploadAvatarBtnLayout button').removeClass('button-light-color').addClass('button-deep-color');
    });
    
    $('#uploadAvatarCropSubmit').addClass('button-deep-color').mouseover(function(){
        $(this).removeClass('button-deep-color').addClass('button-light-color');
    }).mouseout(function(){
        $(this).removeClass('button-light-color').addClass('button-deep-color');
    });
});