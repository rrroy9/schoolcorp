$(document).ready(function() {
    $('#emailInput').on('blur', function() {
      var email = $(this).val();
      if (email) {
        var url = 'checkemail/?email=' + email; // Corrected the URL syntax
        var req = new XMLHttpRequest();
        req.onreadystatechange = function(){
          if (this.readyState == 4) {
            if (this.status == 200) {
              var response = JSON.parse(req.responseText);
              if (response.exists) {
                var errorMessage = 'Email address already exists';
                $('#emailerror').html(errorMessage).addClass('error');
              } else {
                $('#emailerror').html('').removeClass('error');
              }
            } else {
              console.log('Error:', req.status, req.statusText);
            }
          }
        };
        req.open("GET", url, true);
        req.send();
      }
    });
  
    $('#usernameInput').on('blur', function() { // Corrected ID selector to match the input element ID
      var username = $(this).val();
      var url = 'checkusername?username=' + username; // Corrected the URL syntax
      var req = new XMLHttpRequest();
      req.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          if (req.responseText == 'true') {
            var errorMessage = 'Username already exists'; // Define errorMessage before using it
            $('#uname').html(errorMessage).addClass('error-message'); // Corrected ID selector to match the span element ID and added the correct class
          } else {
            $('#uname').html('').removeClass('error-message'); // Corrected ID selector to match the span element ID and removed the correct class
          }
        }
      };
      req.open("GET", url, true); // Open the request
      req.send(); // Send the request
    });
    // $('#openForm').click(function () {
    //   $('#overlay1').show();
    // });
    // $('.close-btn').click(function () {
    //   $('#overlay1').hide();
    //    // Reset the form
    //     location.reload(); // Reload the page
    // });
  
    
  });
  
  
   
  $(document).ready(function() {
    $('#registration-form').submit(function(event) {
      event.preventDefault(); // Prevent default form submission
      
      // Display loading spinner or buffer sign on the button
      $('#otpButton').html('<i class="fa fa-spinner fa-spin"></i> Sending OTP...');
      $('#otpButton').prop('disabled', true); // Disable the button
      
      var email = $('#emailInput').val();
      
  
      // Get CSRF token from cookie
      var csrftoken = getCookie('csrftoken');
  
      // AJAX request to send OTP
      $.ajax({
        url: 'send_otp?email='+email, // Modify URL as needed
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ email: email }),
        headers: {
          'X-CSRFToken': csrftoken
        },
        success: function(response) {
          console.log('Response from server:', response);
          // OTP sent successfully, update UI
          $('#otpButton').html('OTP Sent');
          $('#otpButton').prop('disabled', false); // Re-enable the button
          $('#registration-form').hide(); // Hide registration form
          $('#rg').hide();
          $('#otpForm').show(); // Show OTP entry form
          $('#otp').focus(); // Focus on OTP input field
        },
        error: function(xhr, status, error) {
          // Handle error
          console.error('Failed to send OTP');
          $('#otpButton').html('Send OTP'); // Revert button text on error
          $('#otpButton').prop('disabled', false); // Re-enable the button
        }
      });
    });
  });
  
  $(document).ready(function() {
    $('#otpForm').submit(function(event) {
      event.preventDefault(); // Prevent default form submission
      
      var otp = $('#otp').val();
      var email = $('#emailInput').val();
      var password = $('#passwordInput').val(); // Retrieve password input value
      
       // Debug statement
      
      
      
      // Get CSRF token
      var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
      
      // AJAX request to verify OTP
      $.ajax({
        url: 'verify_otp',
        type: 'POST',
        contentType: 'application/json',
        headers: {
          'X-CSRFToken': csrfToken // Include CSRF token in headers
        },
        data: JSON.stringify({
          otp: otp,
          email: email
        }),
        success: function(response) {
          if (response.status === 'success') {
            var username = $('#usernameInput').val();
            var firstName = $('#first_name').val();
            var lastName = $('#last_name').val();
            
            // Call function to create user
            createUser(password, username, firstName, lastName, email);
          } else {
            console.log('OTP verification failed: ' + response.message);
          }
        },
        error: function(xhr, status, error) {
          console.log('Failed to verify OTP: ' + error);
        }
      });
    });
  });
  
  // Function to create user
  function createUser(password, username, firstName, lastName, email) {
    var csrftoken = getCookie('csrftoken');
  
    // AJAX request to create user
    $.ajax({
      url: 'create_user',
      type: 'POST',
      contentType: 'application/json',
      headers: {
        'X-CSRFToken': csrftoken
      },
      data: JSON.stringify({
        password: password,
        username: username,
        first_name: firstName,
        last_name: lastName,
        email: email
      }),
      success: function(response) {
        console.log('User created successfully');
        $('#otp').hide();
        location.reload();
        // Close OTP form or perform any other necessary actions
      },
      error: function(xhr, status, error) {
        console.log('Failed to create user');
        // Show error message or perform any other necessary actions
      }
    });
  }
  // Function to retrieve CSRF token from cookie
  
  
  
  
  
  
  
  
  // Function to get CSRF token from cookie
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
  
  
  
  const showModal = (openButton, modalContent) =>{
    const openBtn = document.getElementById(openButton),
          modalContainer = document.getElementById(modalContent);
    
    if(openBtn && modalContainer){
        openBtn.addEventListener('click', ()=>{
            modalContainer.classList.add('show-modal');
        });
    }
}

showModal('open-modal','modal-container');

/*=============== CLOSE MODAL ===============*/
const closeBtn = document.querySelectorAll('.close-modal');

function closeModal(){
    const modalContainer = document.getElementById('modal-container');
    modalContainer.classList.remove('show-modal');
    window.location.reload(); // Reload the page
}

closeBtn.forEach(c => c.addEventListener('click', closeModal));
