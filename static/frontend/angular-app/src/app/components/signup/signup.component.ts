import { Component, OnInit } from '@angular/core';
import { SignupService } from '../../services/singup/signup.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css'],
  providers: [SignupService]
})
export class SignupComponent implements OnInit {

  signup: any = {};
  errors: any = {};

  constructor(private signupService : SignupService, private router: Router) { }

  ngOnInit() {
  }

  onSubmit(){
    this.signupService.signup(this.signup).subscribe(
      
      response => {
        alert('User ' + this.signup.username + ' has been created!')
        this.router.navigate(['']);
      },
      errors => this.errors = errors.error
      // error => console.log('errors', error)
    );
  }
}
