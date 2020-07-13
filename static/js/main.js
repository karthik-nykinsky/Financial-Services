function validate(){
    var email = document.getElementById("id_email").value;
    var first_name = document.getElementById("id_first_name").value;
    var last_name = document.getElementById("id_last_name").value;
    var phone = document.getElementById("id_phone").value;
    var company = document.getElementById("id_company").value;
    var pass1 = document.getElementById("id_paasword1").value;
    var pass2 = document.getElementById("id_password2").value;

    if (!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)){
        document.getElementById('error').innerHTML="Invalid Email";
        return true;
    }
    else if(!/[a-Z]+$/.test(first_name)){
        document.getElementById('error').innerHTML="Invalid First Name";
        return true;
    }
    else if(!/[a-Z]+$/.test(last_name)){
        document.getElementById('error').innerHTML="Invalid Last Name";
        return true;
    }
    else if(company === ''){
        document.getElementById('error').innerHTML="Invalid Company Name";
        return true;
    }
    else if(phone.length != 10 || !/[878][0-9]+$/.test(phone)){
        document.getElementById('error').innerHTML="Invalid Phone";
        return true;
    }
    else if(pass1.length < 8){
        document.getElementById('error').innerHTML="Password short";
        return true;
    }
    else if(pass1 != pass2){
        document.getElementById('error').innerHTML="Password Not Matching";
        return true;
    }
    else{
        return false;
    }
};