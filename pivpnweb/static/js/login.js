$(document).ready(function(){

icon_appen_password = `
<div class="input-group-append">
  <div class="input-group-text">
    <span class="fas fa-lock"></span>
  </div>
</div>`
icon_appen_user = `
<div class="input-group-append">
  <div class="input-group-text">
    <span class="fas fa-user"></span>
  </div>
</div>`

div_parent_username = $("#id_username").parent()
div_parent_password = $("#id_password").parent()
div_parent_main = $(div_parent_password).parent()

// Format inputs and title
$($('div.login > h2')[0]).addClass("login-box-msg").css("font-size","1.25rem")
$("#id_username").addClass("form-control").attr("placeholder", "Username")
$("#id_password").addClass("form-control").attr("placeholder", "Password")

$("label[for='id_username']").remove()
$("label[for='id_password']").remove()

$(div_parent_password).addClass("input-group mb-3").append(icon_appen_password)
$(div_parent_username).addClass("input-group mb-3").append(icon_appen_user)

// Sign In button and remember check
$(div_parent_main).append(`
 <div class="row">
  <div class="col-8">
    <div class="icheck-primary">
      <input type="checkbox" id="remember">
      <label for="remember">
        Remember Me
      </label>
    </div>
  </div>
  <div class="col-4" id="button-col"></div>
 </div>`)

$("button.form-submit").text("Sign In").addClass("btn btn-primary btn-block").appendTo("#button-col");
$("button.form-submit").off('click').on('click', function(event){
    if($('#remember').is(":checked"))
    {
        localStorage.setItem('user', $('#id_username').val());
        localStorage.setItem('pass', $('#id_password').val());
        localStorage.setItem('remember', $('#remember').is(":checked"));
    }
    else
    {
        localStorage.clear();
        localStorage.setItem('remember', $('#remember').is(":checked"));
    }
})

// Error message
$("button.close-message").remove();
$("div.alert-error > span").remove()
$("ul.errorlist > li").css("color","red")

// Autocomplete login
if(localStorage.getItem('remember') === 'true')
{
    $('#id_username').val(localStorage.getItem('user'));
    $('#id_password').val(localStorage.getItem('pass'));
    $('#remember').prop('checked', true);
}
})