const BACKEND_URL = 'http://localhost:5000/diarist';

const MIN_PASSWORD_LENGTH = 10;
const MAX_PASSWORD_LENGTH = 25;
const MIN_NAME_LENGTH = 3;
const MAX_NAME_LENGTH = 25;

const form = document.getElementById('signup-form');
const name = document.getElementById('inputName');
const email = document.getElementById('inputEmail');
const password = document.getElementById('inputPassword');
const password2 = document.getElementById('confirmPassword');

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
    showError(input, 'Email is not valid.');
  }
}

// Check input length
function validateLength(input, min, max) {
  if (input.value.length < min) {
    showError(
      input,
      `${getFieldName(input)} must be at least ${min} characters.`
    );
  } else if (input.value.length > max) {
    showError(
      input,
      `${getFieldName(input)} must be less than ${max} characters.`
    );
  } else {
    showSuccess(input);
  }
}

// Check passwords match
function validatePasswordMatch(input1, input2) {
  if (input1.value !== input2.value) {
    showError(input2, 'Passwords do not match.');
  }
}

// Get fieldname
function getFieldName(input) {
  return input.placeholder;
}

// Event listeners
form.addEventListener('submit', function (e) {
  e.preventDefault();
  checkRequiredFields([name, email, password]);
  validateLength(name, MIN_NAME_LENGTH, MAX_NAME_LENGTH);
  validateEmail(email);
  validateLength(password, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH);
  validateLength(password2, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH);
  validatePasswordMatch(password, password2);

  axios
    .post(`${BACKEND_URL}/register`, {
      email: email.value,
      username: name.value,
      password: password.value,
    })
    .then((res) => {
      sessionStorage.setItem('token', res.data.token);
      window.location.href = 'journal.html';
    })
    .catch((err) => {
      console.error(err);
      alert(err);
    });
});
