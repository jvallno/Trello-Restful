import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BoardDetailService {

  baseurl = 'http://127.0.0.1:8000/api/board/';
  emailUrl = 'http://127.0.0.1:8000/api/invite';
  windowUrl = window.location.href;
  httpHeaders = new HttpHeaders({'Content-Type': 'application/json'})
  csrfheaders = new HttpHeaders({'X-CSRFToken': this.cookieService.get('csrftoken')});
  link = {headers: this.httpHeaders};
  csrf = {headers: this.csrfheaders};

  constructor(private http: HttpClient, private cookieService:CookieService) { }

// LIST
  getAllList(id): Observable<any>{
    return this.http.get(this.baseurl + id + '/list/',
    this.link);
  }

  getSingleList(listID, boardID): Observable<any>{
    return this.http.get(this.baseurl + boardID + '/list/' + listID,
    this.link);
  }

  updateSingleList(boardID, listObj): Observable<any>{
    let data = {title: listObj.title}
    return this.http.put(this.baseurl + boardID + '/list/' + listObj.id, data,
    this.link);
  }

  createObjectList(boardID, listObj): Observable<any>{
    const data = {title: listObj.title};
    return this.http.post(this.baseurl + boardID + '/list/', data,
    this.link);
  }

  deleteSelectedList(boardID, listObj): Observable<any>{
    return this.http.delete(this.baseurl + boardID + '/list/' + listObj.id,
    this.link);
  }

// CARD
  getAllCard(boardID, listObj): Observable<any>{
    return this.http.get(this.baseurl + boardID + '/list/' + listObj.id + '/card/',
    this.link);
  }

  getSingleCard(boardID, listID, cardID): Observable<any>{
    return this.http.get(this.baseurl + boardID + '/list/' + listID + '/card/' + cardID,
    this.link);
  }

  getSingledCard(boardID, listID): Observable<any>{
    return this.http.get(this.baseurl + boardID + '/list/' + listID + '/card/',
    this.link);
  }

  updateSingleCard(boardID, cardObj, cardID): Observable<any>{
    let data = {title: cardObj.title}
    return this.http.put(this.baseurl + boardID + '/list/' + cardObj.id + '/card/' + cardID, data,
    this.link);
  }

  createObjectCard(boardID, listObj, cardObj): Observable<any>{
    const data = {title: cardObj.title};
    return this.http.post(this.baseurl + boardID + '/list/' + listObj.id + '/card/', data,
    this.link);
  }

  deleteSelectedCard(boardID, listObj, cardObj): Observable<any>{
    return this.http.delete(this.baseurl + boardID + '/list/' + listObj.id + '/card/' + cardObj.id,
    this.link);
  }

  archiveSelectedList(boardID, listObj): Observable<any>{
    let data = {archive: true}
    return this.http.put(this.baseurl + boardID + '/list/' + listObj.id, data,
    this.link);
  }

  archiveSelectedCard(boardID, listObj, cardObj): Observable<any>{
    let data = {archive: true}
    return this.http.put(this.baseurl + boardID + '/list/' + listObj.id + '/card/' + cardObj.id, data,
    this.link);
  }

  sendInvitationEmail(boardID, emailData): Observable<any>{
    const data = {member_email: emailData.member_emails};
    return this.http.post(this.emailUrl, data,
    this.link);
  }
}
