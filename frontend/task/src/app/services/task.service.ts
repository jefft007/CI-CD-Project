import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class TaskService {

  // RENDER BACKEND URL
  apiUrl = 'https://ci-cd-project-ogqi.onrender.com/tasks';

  constructor(private http: HttpClient) { }

  // GET ALL TASKS
  getTasks() {
    return this.http.get(this.apiUrl);
  }

  // ADD TASK
  addTask(task: any) {
    return this.http.post(this.apiUrl, task);
  }

  // UPDATE TASK
  updateTask(id: string, task: any) {
    return this.http.put(`${this.apiUrl}/${id}`, task);
  }

  // DELETE TASK
  deleteTask(id: string) {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

}