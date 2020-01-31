import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SignupService {

  constructor(private http: HttpClient) { }

  signup(userData:any): Observable<any>{
    return this.http.post('http://127.0.0.1:8000/api/signup/', userData);
  }
}