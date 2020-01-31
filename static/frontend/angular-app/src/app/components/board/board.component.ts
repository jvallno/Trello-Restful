import { Component, OnInit } from '@angular/core';
import { throwError } from 'rxjs';
import { BoardService } from '../../services/board/board.service';
import { UserService } from '../../services/user/user.service';

@Component({
  selector: 'app-board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.css']
})
export class BoardComponent implements OnInit {
  new_board: any;
  boards;

  constructor(private boardService: BoardService, private userService: UserService) { }

  ngOnInit() {
    this.new_board = {
      title: '',
      description: ''
    };
  }


  createBoard() {
    this.boardService.create(this.new_board, this.userService.token).subscribe(
       data => {
         // refresh the list
         return true;
       },
       error => {
         console.error('Error saving!');
         return throwError(error);
       }
    );
  }

}
