import { Component, OnInit } from '@angular/core';
import { TaskService } from '../services/task.service';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  tasks: any[] = [];

  constructor(private taskService: TaskService, private authService: AuthService) { }

  logout() {
    this.authService.logout();
  }

  ngOnInit(): void {
    this.getTasks();
  }

  getTasks() {

    this.taskService.getTasks().subscribe((data: any) => {

      this.tasks = data;

      console.log(this.tasks);

    });

  }

}