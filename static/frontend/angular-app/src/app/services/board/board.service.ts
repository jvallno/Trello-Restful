import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { UserService } from '../user/user.service';

@Injectable({
  providedIn: 'root'
})
export class BoardService {

  constructor(private http: HttpClient, private userService: UserService) { }

  // Uses http.get() to load data from a single API endpoint
  list() {
    return this.http.get('/api/board');
  }
  create(post, token) {
    return this.http.post('/api/board', JSON.stringify(post), this.getHttpOptions());
  }

  // helper function to build the HTTP headers
  getHttpOptions() {
    return {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': 'JWT ' + this.userService.token
      })
    };
  }
}
