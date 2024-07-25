$(document).ready(function() {
      $('#name').on('input', function() {
        var input = $(this).val();
        var errorElement = $('#name-error');

        // Remove any existing validation classes and error message
        $(this).removeClass('valid invalid');
        errorElement.text('');

        // Validate minimum length
        if (input.length < 3) {
          $(this).addClass('invalid');
          errorElement.text('Minimum length is 3 characters.');
          return;
        }

        // Validate maximum length
        if (input.length > 10) {
          $(this).addClass('invalid');
          errorElement.text('Maximum length is 10 characters.');
          return;
        }

        // Validate special characters and numbers
        var specialCharsNumbers = /[^A-Za-z]/;
        if (specialCharsNumbers.test(input)) {
          $(this).addClass('invalid');
          errorElement.text('Special characters and numbers are not allowed.');
          return;
        }

        // Validate spaces
        if (input.indexOf(' ') >= 0) {
          $(this).addClass('invalid');
          errorElement.text('Spaces are not allowed.');
          return;
        }

        // All validations passed, add valid class
        $(this).addClass('valid');
      });
    });

    $(document).ready(function() {
      $('#lname').on('input', function() {
        var input = $(this).val();
        var errorElement = $('#lname-error');

        // Remove any existing validation classes and error message
        $(this).removeClass('valid invalid');
        errorElement.text('');

        // Validate minimum length
        if (input.length < 3) {
          $(this).addClass('invalid');
          errorElement.text('Minimum length is 3 characters.');
          return;
        }

        // Validate maximum length
        if (input.length > 10) {
          $(this).addClass('invalid');
          errorElement.text('Maximum length is 10 characters.');
          return;
        }

        // Validate special characters and numbers
        var specialCharsNumbers = /[^A-Za-z]/;
        if (specialCharsNumbers.test(input)) {
          $(this).addClass('invalid');
          errorElement.text('Special characters and numbers are not allowed.');
          return;
        }

        // Validate spaces
        if (input.indexOf(' ') >= 0) {
          $(this).addClass('invalid');
          errorElement.text('Spaces are not allowed.');
          return;
        }

        // All validations passed, add valid class
        $(this).addClass('valid');
      });
});

$(document).ready(function() {
  // Function to validate mobile number
  function validateMobileNumber(mobileNumber) {
    // Regular expression to check if the mobile number contains only numeric values and has exactly 10 digits
    var regex = /^[0-9]{10}$/;
    return regex.test(mobileNumber);
  }

  // Event listener for input change
  $("#mobileNumber").on("input", function() {
    // Get the entered mobile number
    var mobileNumber = $(this).val();

    // Trim the input to the first 10 digits
    mobileNumber = mobileNumber.slice(0, 10);

    // Update the input value
    $(this).val(mobileNumber);

    // Validate the mobile number
    if (validateMobileNumber(mobileNumber)) {
      // Clear any previous error message
      $("#mobileError").text("");
    } else {
      // Display an error message
      $("#mobileError").text("Please enter a valid 10-digit mobile number (numeric only).");
    }
  });
});

$(document).ready(function() {
  $('#email').on('input', function() {
    var email = $(this).val();
    var isValid = true;
    var errorMessage = '';

    // Check for a valid email format using regular expression
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      isValid = false;
      errorMessage = 'Please enter a valid email address.';
    }

    // Display error message if validation fails
    if (!isValid) {
      $('#email-error').html(errorMessage).addClass('error');
    } else {
      $('#email-error').html('').removeClass('error');
    }
  });
});


$(document).ready(function() {
  $('#password').on('input', function() {
    var password = $(this).val();
    var isValid = true;
    var errorMessage = '';

    // Check for minimum length of 8 characters
    if (password.length < 8) {
      isValid = false;
      errorMessage += 'Password must be at least 8 characters long.<br>';
    }

    // Check for at least 1 uppercase letter
    if (!/[A-Z]/.test(password)) {
      isValid = false;
      errorMessage += 'Password must contain at least 1 uppercase letter.<br>';
    }

    // Check for at least 1 lowercase letter
    if (!/[a-z]/.test(password)) {
      isValid = false;
      errorMessage += 'Password must contain at least 1 lowercase letter.<br>';
    }

    // Check for at least 1 digit
    if (!/\d/.test(password)) {
      isValid = false;
      errorMessage += 'Password must contain at least 1 digit.<br>';
    }

    // Check for no special characters
    if (/[^a-zA-Z0-9]/.test(password)) {
      isValid = false;
      errorMessage += 'Password cannot contain special characters.<br>';
    }

    // Display error message if validation fails
    if (!isValid) {
      $('#password-error').html(errorMessage).addClass('error');
    } else {
      $('#password-error').html('').removeClass('error');
    }
  });
});

$(document).ready(function() {
  $('#username').on('input', function() {
    var username = $(this).val();
    var isValid = true;
    var errorMessage = '';

    // Check for minimum length of 5 characters
    if (username.length < 5) {
      isValid = false;
      errorMessage += 'Username must be at least 5 characters long.<br>';
    }

    // Check for at least 1 uppercase letter
    if (!/[A-Z]/.test(username)) {
      isValid = false;
      errorMessage += 'Username must contain at least 1 uppercase letter.<br>';
    }

    // Check for at least 1 lowercase letter
    if (!/[a-z]/.test(username)) {
      isValid = false;
      errorMessage += 'Username must contain at least 1 lowercase letter.<br>';
    }

    // Check for at least 1 digit
    if (!/\d/.test(username)) {
      isValid = false;
      errorMessage += 'Username must contain at least 1 digit.<br>';
    }

    // Check for no special characters
    if (/[^a-zA-Z0-9]/.test(username)) {
      isValid = false;
      errorMessage += 'Username cannot contain special characters.<br>';
    }

    // Display error message if validation fails
    if (!isValid) {
      $('#username-error').html(errorMessage);
    } else {
      $('#username-error').html('');
    }
  });
});

$(document).ready(function() {
  $('#mname').on('input', function() {
    var input = $(this).val().trim(); // Trim leading and trailing spaces
    var errorElement = $('#mname-error');

    // Remove any existing validation classes and error message
    $(this).removeClass('valid invalid');
    errorElement.text('');

    // Validate minimum length
    if (input.length < 3) {
      $(this).addClass('invalid');
      errorElement.text('Minimum length is 3 characters.');
      return;
    }

    // Validate special characters and numbers
    var specialCharsNumbers = /[^A-Za-z\s]/; // Updated regex to allow spaces (\s)
    if (specialCharsNumbers.test(input)) {
      $(this).addClass('invalid');
      errorElement.text('Special characters and numbers are not allowed.');
      return;
    }

    // All validations passed, add valid class
    $(this).addClass('valid');
  });
});

$(document).ready(function() {
  $('#fname').on('input', function() {
    var input = $(this).val().trim(); // Trim leading and trailing spaces
    var errorElement = $('#fname-error');

    // Remove any existing validation classes and error message
    $(this).removeClass('valid invalid');
    errorElement.text('');

    // Validate minimum length
    if (input.length < 3) {
      $(this).addClass('invalid');
      errorElement.text('Minimum length is 3 characters.');
      return;
    }

    // Validate special characters and numbers
    var specialCharsNumbers = /[^A-Za-z\s]/; // Updated regex to allow spaces (\s)
    if (specialCharsNumbers.test(input)) {
      $(this).addClass('invalid');
      errorElement.text('Special characters and numbers are not allowed.');
      return;
    }

    // All validations passed, add valid class
    $(this).addClass('valid');
  });
});

