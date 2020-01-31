import { Component, OnInit } from '@angular/core';
import { HomeService } from '../../services/home/home.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  providers: [HomeService]
})
export class HomeComponent implements OnInit {

  boards:any = [{}];
  selectBoard: any = {};
  _createBoard:any = {};
  errors: any = [];
  private showHideBtn = true;

  htmlVariable: string = "<b>Some html.</b>";

  constructor(private api : HomeService){
    this.getBoards();
  }
  
  getBoards = () => {
    this.api.getAllBoards().subscribe(
      data => {
        this.boards = data;
      },
      error => {
        this.errors = error
        console.log(error);
      })
  }

  boardClick = (board) => {
    this.api.getSingleBoard(board.id).subscribe(
      data => {
        this.selectBoard = data;
        console.log(data);
      },
      error => {
        this.errors = error
        console.log(error);
      })
  }

  updateBoard = () => {
    this.api.updateSingleBoard(this.selectBoard).subscribe(
      data => {
        this.getBoards();
        document.getElementById("close-btn").click();
        console.log(data);
      },
      error => {
        this.errors = error
        console.log(error);
    })
  }

  createBoard = () => {
    this.api.createBoard(this.selectBoard).subscribe(
      data => {
        this.boards.push(data);
        document.getElementById("close-btn").click();
        console.log(data)
      },
      error => {
        this.errors = error
        console.log(error);
      }
    );
  }

  deleteBoard = () => {
    this.api.deleteSelectedBoard(this.selectBoard.id).subscribe(
      data => {
        this.getBoards();
      },
      error => {
        this.errors = error
        console.log(error);
      }
    );
  }

  boardDetail = () => {
    this.api.getAllBoards().subscribe(
      data => {
        console.log(data);
      },
      error => {
        this.errors = error
        console.log(error);
      }
    )
  }

  ngOnInit() {
  }
}
