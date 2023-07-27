import { TestBed } from '@angular/core/testing';

import { AggsService } from './aggs.service';

describe('AggsService', () => {
  let service: AggsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AggsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
