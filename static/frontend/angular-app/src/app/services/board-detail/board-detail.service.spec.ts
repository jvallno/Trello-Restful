import { TestBed } from '@angular/core/testing';

import { BoardDetailService } from './board-detail.service';

describe('BoardDetailService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: BoardDetailService = TestBed.get(BoardDetailService);
    expect(service).toBeTruthy();
  });
});
