import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HomeService {


  baseurl = 'http://127.0.0.1:8000'
  httpHeaders = new HttpHeaders({'Content-Type': 'application/json'})
  csrfheaders = new HttpHeaders({'X-CSRFToken': this.cookieService.get('csrftoken')});
  link = {headers: this.httpHeaders};
  csrf = {headers: this.csrfheaders};

  constructor(private http: HttpClient, private cookieService:CookieService) { }

  getAllBoards(): Observable<any>{
    return this.http.get(this.baseurl + '/api/board/',
    this.link);
  }

  getSingleBoard(id): Observable<any>{
    return this.http.get(this.baseurl + '/api/board/' + id + '/',
    this.link);
  }

  updateSingleBoard(board): Observable<any>{
    let data = {title: board.title}
    return this.http.put(this.baseurl + '/api/board/' + board.id + '/', data,
    this.link);
  }

  createBoard(boards): Observable<any>{
    const data = {title: boards.title};
    console.log(data)
    return this.http.post(this.baseurl + '/api/board/', data,
    this.link);
  }

  deleteSelectedBoard(id): Observable<any>{
    return this.http.delete(this.baseurl + '/api/board/' + id + '/',
    this.link);
  }
}