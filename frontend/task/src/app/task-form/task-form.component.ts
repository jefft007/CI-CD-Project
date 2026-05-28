import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-task-form',
  templateUrl: './task-form.component.html',
  styleUrls: ['./task-form.component.css']
})
export class TaskFormComponent {
  constructor(private router: Router) {}

  saveTask(event: Event) {
    event.preventDefault();
    // Assuming backend call happens here
    this.router.navigate(['/dashboard']);
  }
}