$(document).ready(function(){

$('form').on('submit', function(event)
{
    event.preventDefault()
    if($('#remember:checked').val() == 'on')
    {
        localStorage.setItem("username", $('#username').val());
        localStorage.setItem("password", $('#password').val());
        localStorage.setItem("remember", "true");
    }
    else
    {
        localStorage.setItem("username", "");
        localStorage.setItem("password", "");
        localStorage.setItem("remember", "false");
    }
    this.submit()
});

// Error message
$("button.close-message").remove();
$("div.alert-error > span").remove()
$("ul.errorlist > li").css("color","red")

// Autocomplete login
if(localStorage.getItem('remember') === 'true')
{
    $('#username').val(localStorage.getItem('username'));
    $('#password').val(localStorage.getItem('password'));
    $('#remember').prop('checked', true);
}

})