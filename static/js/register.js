const usernameField=document.querySelector('#usernameField')
const feedBackArea=document.querySelector('.invalid-feedback')
const submitBtn = document.querySelector('.submit-btn');

usernameField.addEventListener('keyup', (e)=>{
    const usernameVal=e.target.value;

    usernameField.classList.remove('is-invalid')
    feedBackArea.style.display = 'none';

    if(usernameVal.length>0){
        fetch("/authentication/validate-username/", {
        body: JSON.stringify({ username: usernameVal }),
        method: "POST",
    })
            .then(res => res.json())
            .then(data => {
                submitBtn.disabled = false
                if(data.username_error){
                    submitBtn.disabled = true
                    usernameField.classList.add('is-invalid')
                    feedBackArea.style.display = 'block';
                    feedBackArea.innerHTML=  `<p>${data.username_error}</p>`
                }else {
                    submitBtn.setAttribute('disabled');
                }
            })
    }

});
const emailField=document.querySelector('#emailField')
const emailFeedBackArea=document.querySelector('.emailFeedBackArea')

emailField.addEventListener('keyup', (e)=>{
    const emailVal=e.target.value;

    emailField.classList.remove('is-invalid')
    emailFeedBackArea.style.display = 'none';

    if(emailVal.length>0){
        fetch("/authentication/validate-email/", {
        body: JSON.stringify({ email: emailVal }),
        method: "POST",
    })
            .then(res => res.json())
            .then(data => {
                submitBtn.disabled = false
                if(data.email_error){
                    submitBtn.disabled = true
                    emailField.classList.add('is-invalid')
                    emailFeedBackArea.style.display = 'block';
                    emailFeedBackArea.innerHTML=  `<p>${data.email_error}</p>`
                }else{
                    submitBtn.setAttribute('disabled');
                }
            })
    }

});

const showPasswordToggle = document.querySelector('.showPasswordToggle')
const passwordField = document.querySelector('#passwordField', )
const passwordFieldd = document.querySelector('#passwordFieldd')
const handleToggleInput = (e)=>{
    if(showPasswordToggle.textContent==='Show password') {
        showPasswordToggle.textContent = 'Hide password';
        passwordField.setAttribute('type', 'text')
        passwordFieldd.setAttribute('type', 'text')

    }else{
        showPasswordToggle.textContent='Show password';
        passwordField.setAttribute('type', 'password')
        passwordFieldd.setAttribute('type', 'password')
    }
}

showPasswordToggle.addEventListener('click', handleToggleInput)


