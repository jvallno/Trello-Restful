import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { BoardDetailService } from 'src/app/services/board-detail/board-detail.service';

@Component({
  selector: 'app-board-details',
  templateUrl: './board-details.component.html',
  styleUrls: ['./board-details.component.css']
})
export class BoardDetailsComponent implements OnInit {

  lists:any = [{}];
  cards:any = [{}];
  selectList:any = {};
  selectCard:any = {};
  inputEmail:any = {};
  errors: any = [];
  paramData;
  listObj;
  private routeSub: Subscription;
  
  constructor(
    private route: ActivatedRoute,
    private api: BoardDetailService,
    private router: Router
  ) {

    this.ngOnInit();
    this.getList();
    this.getCard();
  }
  
  ngOnInit() {
    this.routeSub = this.route.params.subscribe(
      params => {
        this.paramData = params
      }
    );
  }

// LIST
  getList = () => {
    let boardId = this.paramData.id
    this.api.getAllList(boardId).subscribe(
      data => {
        this.lists = data.map(list => ({...list, boardId}));
      },
      error => {
        this.router.navigate(['login']);
        this.errors = error
        console.log(error);
      })
  }

  listClick = (list) => {
    console.log(list.id+'listClick')
    this.api.getSingleList(list.id, list.boardId).subscribe(
      data => {
        this.selectList = data;
      },
      error => {
        this.errors = error
        console.log(error);
    })
  }

  updateList = () => {
    this.api.updateSingleList(this.paramData.id, this.selectList).subscribe(
      data => {
        document.getElementById("close-btn").click();
        this.getList();
        console.log(data);
      },
      error => {
        this.errors = error
        console.log(error);
    })
  }

  createList = () => {
    this.api.createObjectList(this.paramData.id, this.selectList).subscribe(
      data => {
        this.lists.push(data);
        document.getElementById("close-btn").click();
        this.getList();
        console.log(data)
      },
      error => {
        this.errors = error
        console.log(error);
      }
    );
  }

  deleteList = () => {
    this.api.deleteSelectedList(this.paramData.id, this.selectList).subscribe(
      data => {
        this.getList();
      },
      error => {
        this.errors = error
        console.log(error);
      }
    );
  }

  // CARD
  getCard = () => {
    this.api.getAllCard(this.paramData.id, this.selectList).subscribe(
      data => {
        this.cards = data;
      },
      error => {
        this.errors = error
        console.log(error);
      })
  }

  cardClick = (card, list) => {
    this.listObj=list // put the value of 'list' to 'this.listObj' to use it on createCard()
    console.log(this.listObj, 'this clicked')
    this.api.getSingleCard(this.paramData.id, list.id, card.id).subscribe(
      data => {
        this.selectCard = data;
        console.log(this.selectCard, 'card object')
      },
      error => {
        this.errors = error
        console.log(error);
    })
  }

  cardClicked = (list) => {
    this.listObj=list // put the value of 'list' to 'this.listObj' to use it on createCard()
    console.log(this.listObj, 'this clicked')
    this.api.getSingledCard(this.paramData.id, list.id).subscribe(
      data => {
        this.selectCard = data;
        console.log(this.selectCard, 'card object')
      },
      error => {
        this.errors = error
        console.log(error);
    })
  }

  updateCard = () => {
    this.api.updateSingleCard(this.paramData.id, this.selectCard, this.selectCard.id).subscribe(
      data => {
        this.getCard();
        this.getList();
        document.getElementById("close-card-btn").click();
        console.log(data);
      },
      error => {
        this.errors = error
        console.log(error);
    })
  }

  createCard = () => {
    let inList = this.listObj;
    this.api.createObjectCard(this.paramData.id, inList, this.selectCard).subscribe(
      data => {
        this.selectCard = data
        this.lists.push(data);
        this.getList();
        document.getElementById("close-card-btn").click();
      },
      error => {
        this.errors = error
        console.log(error);
      })
    }

  deleteCard = () => {
    let inList = this.listObj;
    this.api.deleteSelectedCard(this.paramData.id, inList, this.selectCard).subscribe(
      data => {
        this.getList();
      },
      error => {
        this.errors = error
        console.log(error);
      }
    );
  }

  archiveList = (list) => {
    let inList = this.listObj;
    console.log(list, 'list obj')
    console.log(this.paramData.id, 'this.selectCard')
    this.api.archiveSelectedList(this.paramData.id, list).subscribe(
      data => {
        this.getList();
      },
      error => {
        this.errors = error
        console.log(error);
      }
    );
  }

  archiveCard = (card, list) => {
    let inList = this.listObj;
    console.log(card, 'card obj')
    console.log(list, 'list obj')
    console.log(this.paramData.id, 'this.selectCard')
    this.api.archiveSelectedCard(this.paramData.id, list, card).subscribe(
      data => {
        this.getList();
      },
      error => {
        this.errors = error
        console.log(error);
      }
    );
  }

  sendEmail = () => {
    console.log(this.inputEmail, 'email')
    this.api.sendInvitationEmail(this.paramData.id, this.inputEmail).subscribe(
      data => {
        this.lists.push(data);
        console.log(data)
      },
      error => {
        this.errors = error
        console.log(error);
      }
    );
  }

}
