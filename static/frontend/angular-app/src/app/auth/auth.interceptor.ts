import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpHeaders } from "@angular/common/http"
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable()
export class AuthInterceptor implements HttpInterceptor{
    
    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        const authToken = localStorage.getItem("Authorization");
        if(authToken !== null){
            req = req.clone({
                setHeaders:{
                    'Content-Type' : 'application/json',
                    'Authorization' : `Bearer ${authToken}`
                }
            });
        }
        return next.handle(req);
    }
}