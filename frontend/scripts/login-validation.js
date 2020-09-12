//Will need to check database if e-mail exists and password is correct

const MIN_PASSWORD_LENGTH = 10;
const MAX_PASSWORD_LENGTH = 25;

const form = document.getElementById('login-form');
const email = document.getElementById('inputEmail');
const password = document.getElementById('inputPassword');

// Show input error message
function showError(input, message) {
  const formControl = input.parentElement;
  formControl.className = 'form-group error';
  const small = formControl.querySelector('small');
  small.innerText = message;
}

// Show success outline
function showSuccess(input) {
  const formControl = input.parentElement;
  formControl.className = 'form-group success';
}

// Check required fields to apply classes
function checkRequiredFields(inputArr) {
  inputArr.forEach(function (input) {
    console.log(input.value);
    if (input.value.trim() === '') {
      showError(input, `${getFieldName(input)} is required.`);
    } else {
      showSuccess(input);
    }
  });
}

// Check email is valid
function validateEmail(input) {
  const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  if (re.test(input.value.trim())) {
    showSuccess(input);
  } else {
    showError(input, "We don't recognize this e-mail.");
  }
}

// Check input length
function validateLength(input, min, max) {
  if (input.value.length < min || input.value.length > max) {
    showError(input, `${getFieldName(input)} entered is incorrect.`);
  }
}

// Get fieldname
function getFieldName(input) {
  return input.placeholder;
}

// Event listeners
form.addEventListener('submit', function (e) {
  e.preventDefault();
  checkRequiredFields([email, password]);
  validateEmail(email);
  validateLength(password, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH);
});