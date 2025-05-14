document.addEventListener('DOMContentLoaded', () => {
  const emailForm = document.getElementById('email-form');
  const codeForm = document.getElementById('code-form');
  const registerForm = document.getElementById('register-form');
  const updateProfileForm = document.getElementById('update-profile-form');
  const changePasswordForm = document.getElementById('change-password-form');
  const deleteAccountForm = document.getElementById('delete-account-form');
  const passwordResetRequestForm = document.getElementById('password-reset-request-form');
  const passwordResetVerifyForm = document.getElementById('password-reset-verify-form');
  const passwordResetConfirmForm = document.getElementById('password-reset-confirm-form');
  const addIncomeForm = document.getElementById('add-income-form');
  const addExpenseForm = document.getElementById('add-expense-form');
  const historyFilterForm = document.querySelector('.filter-form');

  // Smooth form transitions
  const forms = [
    emailForm, codeForm, registerForm, updateProfileForm, changePasswordForm,
    passwordResetRequestForm, passwordResetVerifyForm, passwordResetConfirmForm,
    addIncomeForm, addExpenseForm, historyFilterForm
  ];
  forms.forEach(form => {
    if (form && !form.classList.contains('form-hidden')) {
      setTimeout(() => {
        form.style.opacity = '1';
      }, 100);
    }
  });

  // Signup Email Form Validation
  if (emailForm) {
    emailForm.addEventListener('submit', (e) => {
      const email = emailForm.querySelector('#email').value;
      if (!email.includes('@')) {
        e.preventDefault();
        alert('Please enter a valid email address.');
      }
    });
  }

  // Signup Code Form Validation
  if (codeForm) {
    codeForm.addEventListener('submit', (e) => {
      const code = codeForm.querySelector('#code').value;
      if (!/^\d{6}$/.test(code)) {
        e.preventDefault();
        alert('Please enter a 6-digit code.');
      }
    });
  }

  // Signup Registration Form Validation
  if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
      const password = registerForm.querySelector('#password').value;
      const confirmPassword = registerForm.querySelector('#confirm_password').value;
      if (password.length < 8) {
        e.preventDefault();
        alert('Password must be at least 8 characters long.');
      } else if (password !== confirmPassword) {
        e.preventDefault();
        alert('Passwords do not match.');
      }
    });
  }

  // Profile Update Form Validation
  if (updateProfileForm) {
    updateProfileForm.addEventListener('submit', (e) => {
      const first_name = updateProfileForm.querySelector('#first_name').value;
      const language = updateProfileForm.querySelector('#preferred_language').value;
      if (!first_name.trim()) {
        e.preventDefault();
        alert('First name is required.');
      }
      if (!language) {
        e.preventDefault();
        alert('Please select a preferred language.');
      }
    });
  }

  // Change Password Form Validation
  if (changePasswordForm) {
    changePasswordForm.addEventListener('submit', (e) => {
      const currentPassword = changePasswordForm.querySelector('#current_password').value;
      const newPassword = changePasswordForm.querySelector('#new_password').value;
      const confirmNewPassword = changePasswordForm.querySelector('#confirm_new_password').value;

      if (!currentPassword || !newPassword || !confirmNewPassword) {
        e.preventDefault();
        alert('All password fields are required.');
      } else if (newPassword !== confirmNewPassword) {
        e.preventDefault();
        alert('New passwords do not match.');
      } else if (newPassword.length < 8) {
        e.preventDefault();
        alert('New password must be at least 8 characters long.');
      }
    });
  }

  // Delete Account Form Confirmation
  if (deleteAccountForm) {
    deleteAccountForm.addEventListener('submit', (e) => {
      if (!confirm('Are you sure you want to delete your account? This cannot be undone.')) {
        e.preventDefault();
      }
    });
  }

  // Password Reset Request Form Validation
  if (passwordResetRequestForm) {
    passwordResetRequestForm.addEventListener('submit', (e) => {
      const email = passwordResetRequestForm.querySelector('#email').value;
      if (!email.includes('@')) {
        e.preventDefault();
        alert('Please enter a valid email address.');
      }
    });
  }

  // Password Reset Verify Form Validation
  if (passwordResetVerifyForm) {
    passwordResetVerifyForm.addEventListener('submit', (e) => {
      const code = passwordResetVerifyForm.querySelector('#code').value;
      if (!/^\d{6}$/.test(code)) {
        e.preventDefault();
        alert('Please enter a 6-digit code.');
      }
    });
  }

  // Password Reset Confirm Form Validation
  if (passwordResetConfirmForm) {
    passwordResetConfirmForm.addEventListener('submit', (e) => {
      const password = passwordResetConfirmForm.querySelector('#password').value;
      const confirmPassword = passwordResetConfirmForm.querySelector('#confirm_password').value;
      if (password.length < 8) {
        e.preventDefault();
        alert('Password must be at least 8 characters long.');
      } else if (password !== confirmPassword) {
        e.preventDefault();
        alert('Passwords do not match.');
      }
    });
  }

  // Add Income Form Validation
  if (addIncomeForm) {
    addIncomeForm.addEventListener('submit', (e) => {
      const amount = addIncomeForm.querySelector('#amount').value;
      const currency = addIncomeForm.querySelector('#currency').value;
      const category = addIncomeForm.querySelector('#category').value;
      const account = addIncomeForm.querySelector('#account').value;

      if (!amount || amount <= 0) {
        e.preventDefault();
        alert('Please enter a positive amount.');
      } else if (!currency) {
        e.preventDefault();
        alert('Please select a currency.');
      } else if (!category) {
        e.preventDefault();
        alert('Please select a category.');
      } else if (!account) {
        e.preventDefault();
        alert('Please select an account.');
      }
    });
  }

  // Add Expense Form Validation
  if (addExpenseForm) {
    addExpenseForm.addEventListener('submit', (e) => {
      const amount = addExpenseForm.querySelector('#amount').value;
      const currency = addExpenseForm.querySelector('#currency').value;
      const category = addExpenseForm.querySelector('#category').value;
      const account = addExpenseForm.querySelector('#account').value;

      if (!amount || amount <= 0) {
        e.preventDefault();
        alert('Please enter a positive amount.');
      } else if (!currency) {
        e.preventDefault();
        alert('Please select a currency.');
      } else if (!category) {
        e.preventDefault();
        alert('Please select a category.');
      } else if (!account) {
        e.preventDefault();
        alert('Please select an account.');
      }
    });
  }

  // History Filter Form Validation
  if (historyFilterForm) {
    historyFilterForm.addEventListener('submit', (e) => {
      const startDate = historyFilterForm.querySelector('#start_date').value;
      const endDate = historyFilterForm.querySelector('#end_date').value;

      if (startDate && endDate && new Date(startDate) > new Date(endDate)) {
        e.preventDefault();
        alert('Start date cannot be later than end date.');
      }
    });
  }

  // Signup Step-by-Step Form Handling
  function initializeSignupForms() {
    const forms = [emailForm, codeForm, registerForm];
    const stepInput = document.querySelector('input[name="step"]');
    const currentStep = stepInput ? stepInput.value : 'email';

    // Debugging: Log the current step
    console.log('Current step:', currentStep);

    // Hide all forms
    forms.forEach(form => {
      if (form) {
        form.classList.remove('active', 'signup-form');
        form.classList.add('signup-form');
      }
    });

    // Show the active form
    if (currentStep === 'email' && emailForm) {
      emailForm.classList.add('active');
      console.log('Showing email form');
    } else if (currentStep === 'code' && codeForm) {
      codeForm.classList.add('active');
      console.log('Showing code form');
    } else if (currentStep === 'register' && registerForm) {
      registerForm.classList.add('active');
      console.log('Showing register form');
    } else {
      // Fallback: Show email form if step is invalid
      if (emailForm) {
        emailForm.classList.add('active');
        console.log('Fallback: Showing email form');
      }
    }
  }

  // Initialize signup forms if on signup page
  if (emailForm || codeForm || registerForm) {
    initializeSignupForms();
  }
});


// Calendar Navigation
function initializeCalendar() {
  const prevMonthBtn = document.getElementById('prev-month');
  const nextMonthBtn = document.getElementById('next-month');
  const currentMonth = new Date(document.querySelector('.calendar-header h2').textContent);

  if (prevMonthBtn) {
    prevMonthBtn.addEventListener('click', () => {
      const prevMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1);
      window.location.href = `/calendar/?year=${prevMonth.getFullYear()}&month=${prevMonth.getMonth() + 1}`;
    });
  }

  if (nextMonthBtn) {
    nextMonthBtn.addEventListener('click', () => {
      const nextMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1);
      window.location.href = `/calendar/?year=${nextMonth.getFullYear()}&month=${nextMonth.getMonth() + 1}`;
    });
  }
}

// Initialize calendar if on calendar page
if (document.querySelector('.calendar-container')) {
  initializeCalendar();
}

// Fetch Incomes via API (Example)
function fetchIncomes(token) {
  fetch('/api/incomes/', {
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json',
    },
  })
    .then(response => response.json())
    .then(data => {
      console.log('Incomes:', data);
      // Update dashboard table with data (implement as needed)
    })
    .catch(error => console.error('Error fetching incomes:', error));
}

// Example: Get Token and Fetch Incomes
function initializeApiCalls() {
  // Replace with actual token retrieval logic (e.g., from login)
  const token = 'your-token-here'; // Implement token storage/retrieval
  if (document.querySelector('.dashboard-table-container')) {
    fetchIncomes(token);
  }
}

// Add to existing DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  // ... existing code ...
  initializeApiCalls();
});

