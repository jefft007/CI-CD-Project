import { Component } from '@angular/core';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent {
  email = '';
  message = '';
  errorMessage = '';
  isLoading = false;

  constructor(private authService: AuthService) {}

  onSubmit(event: Event) {
    event.preventDefault();
    if (!this.email) {
      this.errorMessage = 'Please enter your email';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.message = '';

    this.authService.forgotPassword(this.email).subscribe({
      next: (res) => {
        this.isLoading = false;
        this.message = res.message || 'If an account exists, a reset link has been sent.';
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.error?.message || 'An error occurred. Please try again.';
      }
    });
  }
}
