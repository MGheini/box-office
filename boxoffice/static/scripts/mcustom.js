function validateMemberRegForm() {
	var elements = document.getElementsByClassName("error");
	for(var i = 0; i < elements.length; i++) {
 		elements[i].innerHTML = "";
	}

    var c = checkRequired(document.forms["memberRegForm"]["member_first_name"].value, "member_first_name");
    if(!c) 
    	return false;
    
    c = checkRequired(document.forms["memberRegForm"]["member_last_name"].value, "member_last_name");
	if(!c)
    	return false;

    c = checkRequired(document.forms["memberRegForm"]["gender"].value, "gender");
    if(!c)
        return false;

    c = checkRequired(document.forms["memberRegForm"]["member_username"].value, "member_username");
    if(!c)
        return false;
    
    c = checkRequired(document.forms["memberRegForm"]["member_password"].value, "member_password");
	if(!c)
    	return false;
    
    c = checkRequired(document.forms["memberRegForm"]["member_password2"].value, "member_password2");
	if(!c)
    	return false;
    
    c = checkRequired(document.forms["memberRegForm"]["member_email"].value, "member_email");
	if(!c)
    	return false;
    
    c = checkRequired(document.forms["memberRegForm"]["pre_phone_number"].value, "pre_phone_number");
	if(!c)
    	return false;

    c = checkRequired(document.forms["memberRegForm"]["phone_number"].value, "phone_number");
    if(!c)
        return false;
    
    c = validateEmail(document.forms["memberRegForm"]["member_email"].value, "member_email");
	if(!c)
    	return false;
    
    c = validatePassword(document.forms["memberRegForm"]["member_password"].value, document.forms["memberRegForm"]["member_password2"].value, "member_password", "member_password2");
	if(!c)
    	return false;
}

function validateOrganizerRegForm() {
    var elements = document.getElementsByClassName("error");
    for(var i = 0; i < elements.length; i++) {
        elements[i].innerHTML = "";
    }

    var c = checkRequired(document.forms["organizerRegForm"]["organizer_first_name"].value, "organizer_first_name");
    if(!c) 
        return false;
    
    c = checkRequired(document.forms["organizerRegForm"]["organizer_last_name"].value, "organizer_last_name");
    if(!c)
        return false;

    c = checkRequired(document.forms["organizerRegForm"]["organization_name"].value, "organization_name");
    if(!c)
        return false;

    c = checkRequired(document.forms["organizerRegForm"]["organization_reg_num"].value, "organization_reg_num");
    if(!c)
        return false;

    c = checkRequired(document.forms["organizerRegForm"]["organizer_username"].value, "organizer_username");
    if(!c)
        return false;
    
    c = checkRequired(document.forms["organizerRegForm"]["organizer_password"].value, "organizer_password");
    if(!c)
        return false;
    
    c = checkRequired(document.forms["organizerRegForm"]["organizer_password2"].value, "organizer_password2");
    if(!c)
        return false;
    
    c = checkRequired(document.forms["organizerRegForm"]["organizer_email"].value, "organizer_email");
    if(!c)
        return false;
    
    c = validateEmail(document.forms["organizerRegForm"]["organizer_email"].value, "organizer_email");
    if(!c)
        return false;
    
    c = validatePassword(document.forms["organizerRegForm"]["organizer_password"].value, document.forms["organizerRegForm"]["organizer_password2"].value, "organizer_password", "organizer_password2");
    if(!c)
        return false;
}

function checkRequired(value, inputName) {
	if (value == null || value == "") {
        react(inputName, "این فیلد الزامی است.");
        return false;
    }
    return true;
}

function validateEmail(email, inputName) {
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    if (!re.test(email)) {
    	react(inputName, "رایانامه معتبر نیست.");
    	return false;
    }
    return true;
}

function validatePassword(password, secondPassword, inputName1, inputName2) {
	if (password.length < 6) {
		react(inputName1, "رمز عبور باید حداقل 6 نویسه باشد.");
		return false;
	}

	if (!(password === secondPassword)) {
		react(inputName2, "رمز عبورها یکسان نیستند.");
		return false;
	}
	return true;
}

function react(name, message) {
    if (name === "gender") {
       var element = document.getElementsByName(name);
       target = element[0].parentElement.parentElement.parentElement.parentElement.nextSibling.nextSibling;
       target.innerHTML = message.fontcolor("red");
    }
    else {
	   var element = document.getElementsByName(name);
       target = element[0].parentElement.nextSibling.nextSibling;
	   target.innerHTML = message.fontcolor("red");
    }
}

function validateLoginForm() {
	var r = Math.random();

	if (r < 0.5) {
		var element = document.getElementById("login-btn");
    	element.setAttribute("class", "btn btn-danger btn-block");
    	element.innerHTML = "ورود ناموفّق";
        return false;
	}
}
