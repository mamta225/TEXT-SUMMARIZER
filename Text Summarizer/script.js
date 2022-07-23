/*const Username=document.getElementById('name')
const Password=document.getElementById('password')
const form=document.getElementById('form')
const errorElement=document.getElementById('error')

form.addEventListener('submit',(e)=>{
    let messages=[]
    if(Username.value===''|| Username.value==null|| Username.value.length<6)
        messages.push("Invalid Name")

    if(Password.value.length<=6){
        alert('Password must be longer than 6 characters')
    }

    if(messages.length>0){
        e.preventDefault()
        errorElement.innerText=messages.join(', ')
    }
}) 
*/
var username=document.forms['form']['username'];
var password=document.forms['form']['password'];

var email_error=document.getElementById('email_errror');
var pass_error=document.getElementById('pass_error');

username.addEventListener('textInput',name_verify);
password.addEventListener('textInput',pass_verify);

function validated(){
    if(username.value.length<6)
    {
        username.style.border="1px solid red";
        name_error.style.display="block";
        username.focus();
        return false;
    }
    if(password.value.length>=6)
    {
        password.style.border="1px solid red";
        pass_error.style.display="block";
        username.focus();
        return true;
    }
}

function name_verify(){
    if(username.value.length>=6){
        username.style.border="1px solid silver";
        name_error.style.display="none";
        return true;
    }
}

function pass_verify(){
    if(password.value.length>=6){
        password.style.bprder="1px solid silver";
        pass_error.style.display="none";
        return true;
    }
}
