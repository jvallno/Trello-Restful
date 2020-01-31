import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class UserService {
 
  // http options used for making API calls
  private httpOptions: any;
 
  // the actual JWT token
  token: string;

  // the token expiration date
  token_expires: Date;
 
  // the username of the logged in user
  username: string;
 
  // error messages received from the login attempt
  errors: any = [];
 
  constructor(private http: HttpClient, private router: Router) {
    this.httpOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json'})
    };
  }
 
  // Uses http.post() to get an auth token from djangorestframework-jwt endpoint
  login(data:any) {
    this.http.post('/api-token-auth/', JSON.stringify(data), this.httpOptions).subscribe(
      data => {
        this.updateData(data['token']);
        localStorage.setItem('Authorization',this.token);
        this.router.navigate(['']);
      },
      err => {
        this.errors = err['error'];
      }
    );
  }
 
  // Refreshes the JWT token, to extend the time the user is logged in
  refreshToken() {
    this.http.post('/api-token-refresh/', JSON.stringify({token: this.token}), this.httpOptions).subscribe(
      data => {
        this.updateData(data['token']);
      },
      err => {
        this.errors = err['error'];
      }
    );
  }
 
  logout() {
    this.token = null;
    this.token_expires = null;
    this.username = null;
  }
 
  updateData(token) {
    this.token = token;
    this.errors = [];
 
    // decode the token to read the username and expiration timestamp
    const token_parts = this.token.split(/\./);
    const token_decoded = JSON.parse(window.atob(token_parts[1]));
    // this.token_expires = new Date(token_decoded.exp * 1000);
    this.username = token_decoded.username;
  }
 
}
